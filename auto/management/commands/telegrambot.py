import asyncio
import logging
from typing import Dict

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

from report.models import CarMileageReport

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    LOGIN, VEHICLE_ID, START_DATE, END_DATE, REPORT_TYPE = range(5)

    def handle(self, *args, **options):
        self.run()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sessions: Dict[int, Dict[str, str]] = {}
        self.TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info(context._user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    async def login_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите логин и пароль через пробел")
        return self.LOGIN

    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.split(" ")
        login = text[0]
        password = text[1]
        self.sessions[context._user_id] = {"login": login, "password": password}
        await context.bot.send_message(chat_id=update.effective_chat.id, text="success")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bye")

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command."
        )

    async def report_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context._user_id not in self.sessions:
            await update.message.reply_text("Вы не авторизованы")
            return
        await update.message.reply_text("Введите id автомобиля")
        return self.VEHICLE_ID

    async def vehicle_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._vehicle_id = int(update.message.text)
        await update.message.reply_text("Теперь введите начальную дату (пример формата: 2023-01-01)")
        return self.START_DATE

    async def start_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._start_date = str(update.message.text)
        await update.message.reply_text("Теперь введите конечную дату (пример формата: 2023-01-01)")
        return self.END_DATE

    async def end_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._end_date = str(update.message.text)
        reply_keyboard = [["Подневный", "Помесячный"]]
        await update.message.reply_text(
            "Выберите тип отчета",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="Тип отчета",
            ),
        )
        return self.REPORT_TYPE

    async def report_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        report_text = str(update.message.text)
        if report_text == "Подневный":
            self._report_type = CarMileageReport.DAY
        elif report_text == "Помесячный":
            self._report_type = CarMileageReport.MONTH

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.make_report)
        await update.message.reply_text("Отчет сформирован, вы можете посмотреть его командой /see_report")

        return ConversationHandler.END

    def make_report(self):
        report = CarMileageReport(
            report_type="Отчет по пробегу за период",
            vehicle_id=self._vehicle_id,
            period=self._report_type,
            start_date=self._start_date,
            end_date=self._end_date,
        )
        report.save()
        logger.info(report.pk)
        self._report_id = report.pk

    async def see_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        auth_ = self.sessions[context._user_id]
        r = requests.get(
            f"http://127.0.0.1:8000/auto_api/reports/car-mil-report/{self._report_id}/",
            auth=(auth_["login"], auth_["password"]),
        )
        results = r.json()
        mileage_data = ""
        tmp = {}
        for data in results["mileage_data"]:
            time = data["time"]
            tmp[time] = 0.0

        for data in results["mileage_data"]:
            time = data["time"]
            km = data["value"]
            tmp[time] += float(km)

        for k, v in tmp.items():
            mileage_data += f"время: {k}".ljust(35) + f"пробег: {round(v, 2)} км\n".rjust(10)

        results_format = f"""
        Тип отчета: {results["report_type"]}
        Регистрационный номер авто: {results["registration_number"]}
        Выбранный период: {results["period"]}
        Начальная дата: {results["start_date"]}
        Конечная дата: {results["end_date"]}
{mileage_data}
        """

        await context.bot.send_message(chat_id=update.effective_chat.id, text=results_format)

    def run(self) -> None:
        application = ApplicationBuilder().token(self.TELEGRAM_TOKEN).build()

        start_handler = CommandHandler("start", self.start)
        see_report_handler = CommandHandler("see_report", self.see_report)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo)

        login_handler = ConversationHandler(
            entry_points=[CommandHandler("login", self.login_start)],
            states={
                self.LOGIN: [MessageHandler(filters.TEXT, self.login)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        report_handler = ConversationHandler(
            entry_points=[CommandHandler("make_report", self.report_start)],
            states={
                self.VEHICLE_ID: [MessageHandler(filters.TEXT, self.vehicle_id)],
                self.START_DATE: [MessageHandler(filters.TEXT, self.start_date)],
                self.END_DATE: [MessageHandler(filters.TEXT, self.end_date)],
                self.REPORT_TYPE: [MessageHandler(filters.TEXT, self.report_type)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        unknown_handler = MessageHandler(filters.COMMAND, self.unknown)

        application.add_handler(login_handler)
        application.add_handler(report_handler)
        application.add_handler(see_report_handler)
        application.add_handler(start_handler)
        application.add_handler(echo_handler)
        application.add_handler(unknown_handler)

        application.run_polling()
