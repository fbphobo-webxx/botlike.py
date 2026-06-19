import telebot
import requests

# Your Configuration
API_TOKEN = '8800062443:AAEhoe2RvhTrU-jGpRrNc6gs9anBjn4Z0_A'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['like'])
def handle_like(message):
    # Split the command (e.g., /like ind 5513136279)
    args = message.text.split()
    
    if len(args) < 3:
        bot.reply_to(message, "❌ **Usage:** `/like {region} {uid}`\nExample: `/like ind 5513136279`", parse_mode='Markdown')
        return

    region = args[1]
    uid = args[2]
    
    # Notify user processing
    sent_msg = bot.reply_to(message, "⏳ *Processing your request...*", parse_mode='Markdown')

    # API Call
    api_url = f"https://najmi-ob53-like-api-vvkb.vercel.app/like?uid={uid}&server_name={region}&key=NJM"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        # Mapping the API response to your template
        name = data.get('PlayerNickname', 'N/A')
        likes_before = data.get('LikesbeforeCommand', '0')
        likes_given = data.get('LikesGivenByAPI', '0')
        likes_after = data.get('LikesafterCommand', '0')
        remaining = data.get('remains', 'N/A')

        template = (
            "╔════════◇◆◇════════╗\n"
            "    🎉 LIKE SUCCESSFULLY 👍 \n"
            "╚════════◇◆◇════════╝\n"
            f"👑 Name: {name}\n"
            f"🕹️ UID: {uid}\n"
            f"🌐 Region: {region.upper()}\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"❤️ Likes Before: {likes_before}\n"
            f"🩵 Likes Given: {likes_given}\n"
            f"💚 Likes after: {likes_after}\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Remaining Requests: {remaining}"
        )
        
        bot.edit_message_text(template, chat_id=message.chat.id, message_id=sent_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ **Error Connection to API**\n`{str(e)}`", 
                              chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is now online...")
    bot.infinity_polling()
