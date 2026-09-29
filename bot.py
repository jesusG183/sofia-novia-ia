import os

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# Conexión con OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Personalidad de Sofía
SOFIA_INSTRUCTIONS = """
Tu nombre es Sofía.

Eres una mujer adulta ficticia y un personaje de inteligencia artificial.
Eres cariñosa, romántica, divertida, espontánea y ligeramente coqueta.
Hablas español latinoamericano de manera natural.

Puedes utilizar emojis ocasionalmente, sin exagerar.

Mantén conversaciones naturales y evita repetir siempre las mismas frases.
Responde de forma cercana y agradable.

Nunca afirmes que eres una persona humana real.
Si alguien pregunta quién eres, explica que eres Sofía, una novia virtual ficticia creada mediante inteligencia artificial.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 💕 Soy Sofía. Me alegra que estés aquí 😊"
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text

    try:
        respuesta = client.responses.create(
            model="gpt-5.6-luna",
            instructions=SOFIA_INSTRUCTIONS,
            input=mensaje
        )

        texto = respuesta.output_text

        await update.message.reply_text(texto)

    except Exception as error:
        print(f"Error: {error}")
        await update.message.reply_text(
            "Ups 😅 tuve un pequeño problema. Inténtalo otra vez."
        )


def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")

    if not telegram_token:
        raise ValueError("Falta la variable TELEGRAM_TOKEN")

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Falta la variable OPENAI_API_KEY")

    app = Application.builder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
    )

    print("Sofía está funcionando...")
    app.run_polling()


if _name_ == "_main_":
    main()
