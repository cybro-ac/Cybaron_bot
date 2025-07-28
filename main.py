import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_API")
ADMIN_TELEGRAM_ID = os.getenv("ADMIN_ID")

if BOT_TOKEN or ADMIN_TELEGRAM_ID is None:
	print("Error: BOT_TOKEN or ADMIN_TELEGRAM_ID is not set.")
	exit()

# --- Tool Data ---
TOOLS = {
    "CraxsRAT": {
        "name": "C • CraxsRAT",
        "description": "A powerful remote administration tool that offers extensive capabilities for controlling and monitoring Android devices, It allows users to gain unauthorized access to a target device\n\nأداة إدارة عن بعد قوية توفر إمكانيات واسعة للتحكم في أجهزة أندرويد ومراقبتها، فهي تسمح للمستخدمين بالوصول غير المصرح به إلى جهاز مستهدف\n\n",
        "price": "Free",
    },
    "CypherRAT": {
        "name": "C • CypherRAT",
        "description": "A stealthy remote access trojan specificallty designed to compromise and control Android devices with a focus on data exfilration and covert surveillence\n\nحصان طروادة خفي للوصول عن بعد مصمم خصيصًا لاختراق أجهزة أندرويد والتحكم فيها مع التركيز على استخراج البيانات والمراقبة السرية\n\n",
        "price": "Free",
    },
    "SilverRAT": {
        "name": "C • SilverRAT",
        "description": "A potent remote access trojan specifcally designed to gain comprehensive control over Android devices, enabling attackers to perform extensive surveillence and data exfiltration\n\nحصان طروادة قوي للوصول عن بعد مصمم خصيصًا للحصول على سيطرة شاملة على أجهزة أندرويد، مما يتيح للمهاجمين إجراء مراقبة مكثفة واستخراج البيانات\n\n",
        "price": "Free",
    },
    "ARoid": {
        "name": "C • ARoid Builder",
        "description": "A sophisticated tool designed for crafting custom Android remote access trojans, It provides users with a framework to build malicious applications capable of gaining unauthorized control over Android devices\n\nأداة متطورة مصممة لإنشاء أحصنة طروادة مخصصة للوصول عن بعد إلى أجهزة أندرويد، وهي توفر للمستخدمين إطار عمل لبناء تطبيقات ضارة قادرة على الحصول على سيطرة غير مصرح بها على أجهزة أندرويد\n\n",
        "price": "$2 USD",
    },
    "Spider": {
        "name": "C • Spider Script",
        "description": "A script to freeze iPhone and Android phones and stop them from working for an unlimited time by phone number through WhatsApp, The user cannot use the phone until it is turned off\n\nسكربت لتجميد هواتف الايفون والاندرويد وايقافها عن العمل لمدة غير محدودة عن طريق رقم الهاتف من خلال الواتس اب ولا يستطيع المستخدم استخدام الهاتف الا بعد اغلاقه\n\n",
        "price": "$2 USD",
    },
    "EagleSpy": {
        "name": "C • EagleSpy",
        "description": "A sophisticated remote access trojan designed to coverty monitor and control Android devices, It provides an attacker with extensive capabilities to spy on a target\n\nحصان طروادة متطور للوصول عن بعد مصمم لمراقبة أجهزة أندرويد والتحكم فيها بشكل سري، ويوفر للمهاجم قدرات واسعة للتجسس على الهدف\n\n",
        "price": "$2 USD",
    },
    "ZeroTrace": {
        "name": "C • ZeroTrace Stealer",
        "description": "A malware designed to gather sensitive information from systems, It boasts capabilities such as harvesting credentials, financial data, and personal files, often employing sophisticated evasion techniques to avoid detection by security software\n\nبرنامج ضار مصمم لجمع معلومات حساسة من الأنظمة، ويتميز بقدرات مثل حصاد بيانات الاعتماد والبيانات المالية والملفات الشخصية، وغالبًا ما يستخدم تقنيات التهرب المتطورة لتجنب اكتشافه بواسطة برامج الأمان\n\n",
        "price": "$2 USD",
    },
    "Reccoon": {
        "name": "C • Reccoon Stealer",
        "description": "A prevalent and dangerous information stealing malware, It specializes in illicitly collecting a wide range of sensitive user data from infected systems, including browser credentials, various system details\n\nبرنامج ضار خطير ومنتشر لسرقة المعلومات، وهو متخصص في جمع مجموعة واسعة من بيانات المستخدم الحساسة بشكل غير قانوني من الأنظمة المصابة، بما في ذلك بيانات اعتماد المتصفح وتفاصيل النظام المختلفة\n\n",
        "price": "$2 USD",
    },
    "Vidar": {
        "name": "C • Vidar Stealer",
        "description": "A information stealing malware, widely available as Malware as a Service MaaS, designed to illicitly collect a vast array of sensitive data from systems, Often employs sophisticated evasion technigues, and can also act as a downloader for other malware\n\nبرنامج ضار لسرقة المعلومات، متوفر على نطاق واسع كخدمة Malware as a Service MaaS، مصمم لجمع مجموعة كبيرة من البيانات الحساسة من الأنظمة بشكل غير قانوني، وغالبًا ما يستخدم تقنيات التهرب المتطورة، ويمكنه أيضًا أن يعمل كأداة تنزيل لبرامج ضارة أخرى\n\n",
        "price": "$2 USD",
    },
    "RedLine": {
        "name": "C • RedLine Stealer",
        "description": "A malicious software categorized as an information stealer, It is designed to covertly collect sensitive data from infected computers and transmit it to an attacker, This data can include a wide range of personal and financial information\n\nبرنامج ضار يُصنف ضمن برامج سرقة المعلومات، تم تصميمه لجمع البيانات الحساسة بشكل سري من أجهزة الكمبيوتر المصابة وإرسالها إلى المهاجم، يمكن أن تشمل هذه البيانات مجموعة واسعة من المعلومات الشخصية والمالية\n\n",
        "price": "$2 USD",
    },
    "Loki": {
        "name": "C • Loki Stealer",
        "description": "Known as LokiBot, is a notorious malicious software primarily designed to steal sensitive information from compromised computers, It can collect various credentials, including usernames, passwords, cryptocurrency wallet data, and other confidential files\n\nمعروف باسم LokiBot، هو برنامج خبيث سيء السمعة مصمم بشكل أساسي لسرقة المعلومات الحساسة من أجهزة الكمبيوتر المخترقة، يمكنه جمع بيانات اعتماد مختلفة، بما في ذلك أسماء المستخدمين وكلمات المرور وبيانات محافظ العملات المشفرة، وملفات سرية أخرى\n\n",
        "price": "$2 USD",
    },
    "Pegasus": {
        "name": "C • Pegasus Spyware",
        "description": "A highly sophisticated and invasive spyware developed by the Israeli cyber arms company NSO Group. It's designed to be covertly installed on mobile phones and other devices running most versions of iOS and Android, Once installed, Pegasus can monitor all activities on the device, including reading text messages, listening to calls, collecting passwords, tracking locations, accessing the target device's microphone and camera, and harvesting information from apps, It's known for its 'Zero Click' exploit capabilities, meaning it can infect a device without any interaction from the target\n\nبرنامج تجسس شديد التطور والتطفل، تم تطويره بواسطة شركة NSO Group الإسرائيلية للأسلحة السيبرانية، تم تصميمه ليتم تثبيته سراً على الهواتف المحمولة والأجهزة الأخرى التي تعمل بمعظم إصدارات iOS وأندرويد، بمجرد تثبيته، يمكن لبيغاسوس مراقبة جميع الأنشطة على الجهاز، بما في ذلك قراءة الرسائل النصية، والاستماع إلى المكالمات، وجمع كلمات المرور، وتتبع المواقع، والوصول إلى ميكروفون وكاميرا الجهاز المستهدف، وجمع المعلومات من التطبيقات، يشتهر بقدراته على الاستغلال 'بدون نقرة'، مما يعني أنه يمكنه إصابة الجهاز دون أي تفاعل من الهدف\n\n",
        "price": "$10 USD",
    },
    "E Checker": {
        "name": "C • Email Checker",
        "description": "A tool for searching for people's information and their Email accounts using an interactive and easy to use user interface on Windows\n\nأداة للبحث عن معلومات الأشخاص وحسابات البريد الإلكتروني الخاصة بهم باستخدام واجهة مستخدم تفاعلية وسهلة الاستخدام على نظام التشغيل ويندوز\n\n",
        "price": "$2 USD",
    },
    "G700": {
        "name": "C • G700",
        "description": "A remote access trojan primarilly known for its extensive capabilties in surveillance, data exfiltration, and remote control over compromised systems It allows attackers to covertly monitor user activity\n\nإن حصان طروادة الوصول عن بعد معروف بقدراته الواسعة في المراقبة وتسلل البيانات والتحكم عن بعد على الأنظمة المخترقة، يسمح للمهاجمين بمراقبة نشاط المستخدم سرا\n\n",
        "price": "$2 USD",
    },
    "XWorm": {
        "name": "C • XWorm RAT",
        "description": "A dangerous type of malware, primarily functioning as a Remote Access Trojan, It allows cybercriminals to gain unauthorized control over a victim's computer from a distance, XWorm is known for its wide range of capabilities, including stealing sensitive data like passwords and cryptocurrency information, logging keystrokes, and even deploying additional malicious payloads like ransomware\n\nنوع خطير من البرامج الضارة، يعمل بشكل أساسي كـ حصان طروادة للوصول عن بعد. يتيح للمجرمين السيبرانيين السيطرة غير المصرح بها على جهاز الكمبيوتر الخاص بالضحية عن بعد، يشتهر XWorm بمجموعة واسعة من الإمكانيات، بما في ذلك سرقة البيانات الحساسة مثل كلمات المرور ومعلومات العملات المشفرة، وتسجيل ضغطات المفاتيح keystrokes، وحتى نشر حمولات خبيثة إضافية مثل برامج الفدية ransomware\n\n",
        "price": "$2 USD",
    },
    "SpyDroid": {
        "name": "C • SpyDroid RAT",
        "description": "An Android application that allows users to monitor various activities on a target device, It can track call logs, SMS messages, location data, installed applications, and more, often operating discreetly in the background, It is primarily marketed for parental control or employee monitoring\n\nسبايدرويد هو تطبيق أندرويد يسمح للمستخدمين بمراقبة الأنشطة المختلفة على جهاز مستهدف، يمكنه تتبع سجلات المكالمات، ورسائل SMS، وبيانات الموقع، والتطبيقات المثبتة، والمزيد، وغالبًا ما يعمل بشكل سري في الخلفية، يتم تسويقه بشكل أساسي لأغراض الرقابة الأبوية أو مراقبة الموظفين\n\n",
        "price": "$2 USD",
    },
}

def generate_tool_keyboard(tools_dict, items_per_row=3):
    keyboard = []
    current_row = []
    for i, (tool_id, tool_info) in enumerate(tools_dict.items()):
        current_row.append(InlineKeyboardButton(tool_id, callback_data=f"show_tool_{tool_id}"))
        if (i + 1) % items_per_row == 0:
            keyboard.append(current_row)
            current_row = []
    if current_row:
        keyboard.append(current_row)
    return InlineKeyboardMarkup(keyboard)


# --- Handlers ---

async def start(update: Update, context) -> None:
    welcome_message = (
        "🟢 🔴 C • Welcome\n\nThis bot offers the latest and most powerful tools at incredibly discounted prices.\n\nيقدم هذا البوت أحدث وأقوى الأدوات بأسعار مخفضة بشكل لا يصدق.\n\n"
    )
    reply_markup = generate_tool_keyboard(TOOLS, items_per_row=3)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def show_tool_details(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    tool_id = query.data.replace("show_tool_", "")
    tool_info = TOOLS.get(tool_id)

    if tool_info:
        details_message = (
            f"🟢 *{tool_info['name']}*\n\n"
            f"{tool_info['description']}\n"
            f"Price: *{tool_info['price']}*\n"
        )

        keyboard = [
            [InlineKeyboardButton(f"Get Tool for {tool_info['price']}", callback_data=f"request_tool_{tool_id}")],
            [InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(details_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.edit_message_text("Error: Tool not found.", parse_mode=ParseMode.MARKDOWN_V2)

async def request_tool(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    tool_id = query.data.replace("request_tool_", "")
    tool_info = TOOLS.get(tool_id)
    user = query.from_user

    if tool_info and ADMIN_TELEGRAM_ID:
        escaped_full_name = escape_markdown(user.full_name, version=2)
        escaped_username = escape_markdown(user.username or 'N/A', version=2)
        escaped_tool_name = escape_markdown(tool_info['name'], version=2)

        notification_message = (
            f"➕ *C • Request* \n\n"
            f"Name: {escaped_full_name}\n"
            f"User: @{escaped_username}\n"
            f"ID: `{user.id}`\n"
            f"Tool: *{escaped_tool_name}*"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=notification_message, parse_mode=ParseMode.MARKDOWN_V2)
            await query.edit_message_text(
                "🟢 C • Notification\n\nYour request has been sent! We will contact you shortly.\n\nتم إرسال طلبك! سنتواصل معك قريبًا.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_main_menu")]])
            )
        except Exception as e:
            logger.error(f"Failed to send notification to admin: {e}")
            await query.edit_message_text(
                "🔴 C • Notification\n\nAn error occurred while sending your request. Please try again later.\n\nحدث خطأ أثناء إرسال طلبك. يُرجى المحاولة لاحقًا.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_main_menu")]])
            )
    else:
        await query.edit_message_text("Error: Could not process request or admin ID not configured.", parse_mode=ParseMode.MARKDOWN_V2)


async def back_to_main_menu(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    welcome_message = (
        "🟢 🔴 C • Welcome\n\nThis bot offers the latest and most powerful tools at incredibly discounted prices.\n\nيقدم هذا البوت أحدث وأقوى الأدوات بأسعار مخفضة بشكل لا يصدق."
    )
    reply_markup = generate_tool_keyboard(TOOLS, items_per_row=3)
    await query.edit_message_text(welcome_message, reply_markup=reply_markup)

# --- Main function to run the bot ---
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(show_tool_details, pattern=r"^show_tool_"))
    application.add_handler(CallbackQueryHandler(request_tool, pattern=r"^request_tool_"))
    application.add_handler(CallbackQueryHandler(back_to_main_menu, pattern="^back_to_main_menu$"))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
