# -*- coding: utf-8 -*- # Ensure UTF-8 encoding for Arabic text
import flet as ft
import sqlite3
import re
import speech_recognition as sr
import threading
import os

# =======================
# Localization (i18n) Setup (No changes needed here)
# =======================
LANGUAGES = {
    "ar": {
        # ... (Keep all translations as before) ...
        "app_title": "VF Cash Helper",
        "toggle_language": "English",
        "error": "خطأ",
        "success": "نجاح",
        "cancel": "إلغاء",
        "save": "حفظ",
        "delete": "حذف",
        "edit": "تعديل",
        "confirm_delete_title": "تأكيد الحذف",
        "confirm_delete_content": "هل أنت متأكد أنك تريد حذف:\n{name}\n({phone})؟",
        "search_placeholder": "بحث بالاسم أو الرقم...",
        "clear_search_tooltip": "مسح البحث",
        "no_contacts": "لا توجد جهات اتصال لعرضها.",
        "mic_permission_note": "قد يطلب نظام التشغيل الإذن لاستخدام الميكروفون عند أول استخدام.",
        "listening": "الاستماع...",
        "recognizing": "جاري التعرف...",
        "speech_timeout": "لم يتم اكتشاف أي كلام.",
        "mic_error": "خطأ في الميكروفون: {e}. تأكد من توصيله ومنح الإذن.",
        "speech_unintelligible": "لم يتم فهم الصوت.",
        "speech_request_error": "خطأ في خدمة التعرف: {e}. تحقق من اتصال الإنترنت.",
        "speech_unexpected_error": "خطأ غير متوقع في التعرف: {e}",
        "speech_recognized_prompt": "تم التعرف على: {text}",
        "speech_recognized_number": "تم التعرف على الرقم: {number}",
        "speech_no_digits": "لم يتم التعرف على أرقام في الكلام.",
        "speech_error_snackbar": "حدث خطأ أثناء محاولة التعرف على الصوت.",
        "launch_url_error": "خطأ: لم يتمكن التطبيق من فتح برنامج الاتصال. {ex}",
        "generic_error_snackbar": "حدث خطأ غير متوقع.",
        "fields_cleared": "تم مسح الحقول.",
        "main_view_title": "تحويل فودافون كاش",
        "phone_label": "رقم الهاتف",
        "phone_hint": "أدخل 11 رقمًا يبدأ بـ 01",
        "confirm_phone_label": "إعادة إدخال رقم الهاتف",
        "amount_label": "المبلغ",
        "amount_hint": "أدخل المبلغ المراد تحويله",
        "send_button": "إرســــال",
        "clear_button": "مسح الحقول",
        "contacts_button": "إدارة جهات الاتصال",
        "mic_tooltip": "إدخال رقم الهاتف صوتيًا",
        "validation_invalid_phone": "⚠️ رقم الهاتف غير صحيح (11 رقمًا مصريًا).",
        "validation_mismatch_phone": "⚠️ الأرقام المدخلة غير متطابقة.",
        "validation_confirm_phone_missing": "⚠️ الرجاء تأكيد رقم الهاتف.",
        "validation_invalid_amount": "⚠️ الرجاء إدخال مبلغ صحيح (أرقام موجبة فقط).",
        "validation_amount_missing": "⚠️ الرجاء إدخال المبلغ.",
        "validation_all_fields_missing": "⚠️ الرجاء إكمال جميع الحقول بشكل صحيح.",
        "validation_incomplete": "⚠️ الرجاء إكمال جميع الحقول.",
        "validation_ok": "✅ البيانات صحيحة وجاهزة للإرسال.",
        "sending_snackbar": "جاري محاولة إرسال {amount} جنيه إلى {phone}...",
        "send_error_snackbar": "خطأ: البيانات غير صالحة للإرسال.",
        "contacts_view_appbar_title": "جهات الاتصال",
        "contacts_view_title": "إدارة جهات الاتصال",
        "add_contact_card_title": "إضافة جهة اتصال جديدة",
        "add_contact_name_label": "الاسم",
        "add_contact_phone_label": "رقم الهاتف (11 رقم)",
        "add_contact_button": "إضافة جهة اتصال",
        "contact_list_title": "قائمة جهات الاتصال",
        "back_button": "الرجوع للرئيسية",
        "balance_button": "استعلام عن الرصيد",
        "balance_snackbar": "جاري محاولة الاستعلام عن الرصيد...",
        "edit_contact_dialog_title": "تعديل جهة اتصال",
        "edit_contact_name_label": "الاسم",
        "edit_contact_phone_label": "رقم الهاتف",
        "edit_save_button": "حفظ التعديلات",
        "delete_contact_menu": "حذف",
        "edit_contact_menu": "تعديل",
        "select_contact_menu": "اختيار للتحويل",
        "options_menu_tooltip": "خيارات",
        "db_add_success": "تمت إضافة جهة الاتصال بنجاح!",
        "db_add_duplicate": "رقم الهاتف موجود بالفعل.",
        "db_add_fail_validation": "الاسم ورقم الهاتف مطلوبان.",
        "db_add_fail_phone_format": "رقم الهاتف يجب أن يبدأ بـ 01 ويتكون من 11 رقمًا.",
        "db_update_success": "تم تحديث جهة الاتصال بنجاح!",
        "db_update_fail_validation": "الاسم ورقم الهاتف الجديدان مطلوبان.",
        "db_update_fail_phone_format": "رقم الهاتف الجديد يجب أن يبدأ بـ 01 ويتكون من 11 رقمًا.",
        "db_update_fail_duplicate": "رقم الهاتف الجديد موجود بالفعل لجهة اتصال أخرى.",
        "db_update_fail_not_found": "لم يتم العثور على جهة الاتصال الأصلية للتحديث.",
        "db_delete_success": "تم حذف جهة الاتصال بنجاح!",
        "db_delete_fail_not_found": "لم يتم العثور على جهة الاتصال.",
        "db_delete_fail_invalid": "رقم الهاتف المطلوب حذفه غير صالح.",
        "db_generic_error": "خطأ غير متوقع: {e}",
        "db_edit_fail_no_data": "خطأ: لا يمكن العثور على بيانات التعديل.",
        "db_edit_fail_components": "خطأ: مكونات نافذة التعديل غير جاهزة.",
        "db_edit_fail_no_id": "خطأ: لا يمكن العثور على معرّف جهة الاتصال للتعديل.",
         "db_fetch_error": "Error fetching contacts: {e}",
         "db_create_error": "Error creating database: {e}",
         "db_update_unexpected_error": "خطأ غير متوقع أثناء التحديث: {e}",
         "db_delete_unexpected_error": "خطأ غير متوقع أثناء الحذف: {e}",
         "dialog_show_error": "خطأ في عرض نافذة التعديل.",

    },
    "en": {
         # ... (Keep all translations as before) ...
        "app_title": "VF Cash Helper",
        "toggle_language": "العربية",
        "error": "Error",
        "success": "Success",
        "cancel": "Cancel",
        "save": "Save",
        "delete": "Delete",
        "edit": "Edit",
        "confirm_delete_title": "Confirm Deletion",
        "confirm_delete_content": "Are you sure you want to delete:\n{name}\n({phone})?",
        "search_placeholder": "Search by name or number...",
        "clear_search_tooltip": "Clear search",
        "no_contacts": "No contacts to display.",
        "mic_permission_note": "The OS may ask for microphone permission on first use.",
        "listening": "Listening...",
        "recognizing": "Recognizing...",
        "speech_timeout": "No speech detected.",
        "mic_error": "Microphone error: {e}. Ensure it's connected and permissions are granted.",
        "speech_unintelligible": "Could not understand audio.",
        "speech_request_error": "Recognition service error: {e}. Check internet connection.",
        "speech_unexpected_error": "Unexpected recognition error: {e}",
        "speech_recognized_prompt": "Recognized: {text}",
        "speech_recognized_number": "Recognized number: {number}",
        "speech_no_digits": "No digits were recognized in the speech.",
        "speech_error_snackbar": "An error occurred during speech recognition.",
        "launch_url_error": "Error: Could not launch dialer application. {ex}",
        "generic_error_snackbar": "An unexpected error occurred.",
        "fields_cleared": "Fields cleared.",
        "main_view_title": "Vodafone Cash Transfer",
        "phone_label": "Phone Number",
        "phone_hint": "Enter 11 digits starting with 01",
        "confirm_phone_label": "Confirm Phone Number",
        "amount_label": "Amount",
        "amount_hint": "Enter the amount to transfer",
        "send_button": "Send",
        "clear_button": "Clear Fields",
        "contacts_button": "Manage Contacts",
        "mic_tooltip": "Voice input for phone number",
        "validation_invalid_phone": "⚠️ Invalid phone number (11 Egyptian digits).",
        "validation_mismatch_phone": "⚠️ Entered numbers do not match.",
        "validation_confirm_phone_missing": "⚠️ Please confirm the phone number.",
        "validation_invalid_amount": "⚠️ Please enter a valid amount (positive numbers only).",
        "validation_amount_missing": "⚠️ Please enter the amount.",
        "validation_all_fields_missing": "⚠️ Please fill all fields correctly.",
        "validation_incomplete": "⚠️ Please complete all fields.",
        "validation_ok": "✅ Data is valid and ready to send.",
        "sending_snackbar": "Attempting to send {amount} EGP to {phone}...",
        "send_error_snackbar": "Error: Data is invalid for sending.",
        "contacts_view_appbar_title": "Contacts",
        "contacts_view_title": "Manage Contacts",
        "add_contact_card_title": "Add New Contact",
        "add_contact_name_label": "Name",
        "add_contact_phone_label": "Phone Number (11 digits)",
        "add_contact_button": "Add Contact",
        "contact_list_title": "Contact List",
        "back_button": "Back to Main",
        "balance_button": "Check Balance",
        "balance_snackbar": "Attempting to check balance...",
        "edit_contact_dialog_title": "Edit Contact",
        "edit_contact_name_label": "Name",
        "edit_contact_phone_label": "Phone Number",
        "edit_save_button": "Save Changes",
        "delete_contact_menu": "Delete",
        "edit_contact_menu": "Edit",
        "select_contact_menu": "Select for Transfer",
        "options_menu_tooltip": "Options",
        "db_add_success": "Contact added successfully!",
        "db_add_duplicate": "Phone number already exists.",
        "db_add_fail_validation": "Name and phone number are required.",
        "db_add_fail_phone_format": "Phone number must start with 01 and be 11 digits long.",
        "db_update_success": "Contact updated successfully!",
        "db_update_fail_validation": "New name and phone number are required.",
        "db_update_fail_phone_format": "New phone number must start with 01 and be 11 digits long.",
        "db_update_fail_duplicate": "New phone number already exists for another contact.",
        "db_update_fail_not_found": "Original contact not found for update.",
        "db_delete_success": "Contact deleted successfully!",
        "db_delete_fail_not_found": "Contact not found.",
        "db_delete_fail_invalid": "Invalid phone number provided for deletion.",
        "db_generic_error": "Unexpected error: {e}",
        "db_edit_fail_no_data": "Error: Cannot find edit data.",
        "db_edit_fail_components": "Error: Edit dialog components are not ready.",
        "db_edit_fail_no_id": "Error: Cannot find contact ID for editing.",
        "db_fetch_error": "Error fetching contacts: {e}",
        "db_create_error": "Error creating database: {e}",
        "db_update_unexpected_error": "Unexpected error during update: {e}",
        "db_delete_unexpected_error": "Unexpected error during deletion: {e}",
        "dialog_show_error": "Error showing edit dialog.",
    },
}

current_lang = "ar"

def get_text(key, **kwargs):
    try:
        text = LANGUAGES.get(current_lang, LANGUAGES["en"]).get(key, f"<{key}>")
        if kwargs:
            return text.format(**kwargs)
        return text
    except KeyError:
        print(f"Warning: Translation key '{key}' not found in language '{current_lang}' or fallback 'en'.")
        return f"<{key}>"
    except Exception as e:
        print(f"Error getting text for key '{key}': {e}")
        return f"<{key}_error>"


DB_NAME = "contacts.db"
selected_phone = None

# =======================
# Database Functions (No changes needed here)
# =======================
def create_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("Database checked/created successfully.")
    except Exception as e:
        print(get_text("db_create_error", e=e))


def fetch_contacts(filter_text=""):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if filter_text:
            query = "SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ? ORDER BY name COLLATE NOCASE ASC"
            search_term = f"%{filter_text}%"
            cursor.execute(query, (search_term, search_term))
        else:
            cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name COLLATE NOCASE ASC")
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    except Exception as e:
        print(get_text("db_fetch_error", e=e))
        return []

def validate_phone_format(phone: str) -> bool:
    if not phone:
        return False
    return bool(re.fullmatch(r"01[0125]\d{8}", phone.strip()))

def add_contact(name: str, phone: str) -> tuple[bool, str]:
    name = name.strip()
    phone = phone.strip()
    if not name or not phone:
        return False, get_text("db_add_fail_validation")
    if not validate_phone_format(phone):
        return False, get_text("db_add_fail_phone_format")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()
        return True, get_text("db_add_success")
    except sqlite3.IntegrityError:
        return False, get_text("db_add_duplicate")
    except Exception as e:
        return False, get_text("db_generic_error", e=e)
    finally:
        conn.close()


def update_contact_by_id(contact_id: int, new_name: str, new_phone: str) -> tuple[bool, str]:
    new_name = new_name.strip()
    new_phone = new_phone.strip()
    if not new_name or not new_phone:
        return False, get_text("db_update_fail_validation")
    if not validate_phone_format(new_phone):
        return False, get_text("db_update_fail_phone_format")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM contacts WHERE phone = ? AND id != ?", (new_phone, contact_id))
        existing = cursor.fetchone()
        if existing:
            return False, get_text("db_update_fail_duplicate")

        cursor.execute("UPDATE contacts SET name = ?, phone = ? WHERE id = ?", (new_name, new_phone, contact_id))
        conn.commit()
        updated_rows = cursor.rowcount
        if updated_rows > 0:
            return True, get_text("db_update_success")
        else:
            return False, get_text("db_update_fail_not_found")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
             return False, get_text("db_update_fail_duplicate")
        return False, get_text("db_update_unexpected_error", e=e)
    finally:
        conn.close()

def delete_contact_by_id(contact_id: int) -> tuple[bool, str]:
    if not isinstance(contact_id, int) or contact_id <= 0:
         return False, get_text("db_delete_fail_invalid")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            return True, get_text("db_delete_success")
        else:
            return False, get_text("db_delete_fail_not_found")
    except Exception as e:
        return False, get_text("db_delete_unexpected_error", e=e)
    finally:
        conn.close()

# =======================
# Speech Recognition Function (No functional changes needed)
# =======================
recognizer = sr.Recognizer()

def recognize_speech_thread(status_callback, result_callback):
    def run():
        status_callback(get_text("listening"))
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            except sr.WaitTimeoutError:
                status_callback(get_text("speech_timeout"))
                result_callback(None, False)
                return
            except OSError as e:
                 status_callback(get_text("mic_error", e=e))
                 result_callback(None, False)
                 return
            except Exception as e:
                 status_callback(get_text("mic_error", e=e))
                 result_callback(None, False)
                 return

        status_callback(get_text("recognizing"))
        try:
            # Determine language code for speech recognition
            sr_lang_code = "ar-EG" if current_lang == "ar" else "en-US"
            text = recognizer.recognize_google(audio, language=sr_lang_code)
            digits = ''.join(filter(str.isdigit, text))
            status_callback(get_text("speech_recognized_prompt", text=text))
            result_callback(digits if digits else "", True)
        except sr.UnknownValueError:
            status_callback(get_text("speech_unintelligible"))
            result_callback("", False)
        except sr.RequestError as e:
            status_callback(get_text("speech_request_error", e=e))
            result_callback(None, False)
        except Exception as e:
            status_callback(get_text("speech_unexpected_error", e=e))
            result_callback(None, False)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

# =======================
# UI Helper Functions (Updated ft.Colors)
# =======================
def show_snackbar(page: ft.Page, message: str, is_error: bool = False):
    if not page: return
    try:
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, text_align=ft.TextAlign.START if current_lang == 'en' else ft.TextAlign.RIGHT),
                # Using updated ft.Colors
                bgcolor=ft.Colors.RED_ACCENT_700 if is_error else ft.Colors.GREEN_ACCENT_700,
                duration=3500,
                show_close_icon=True
            )
        )
    except Exception as e:
        print(f"Error showing SnackBar: {e}")

def close_specific_dialog(page: ft.Page, dialog: ft.AlertDialog):
    if page and dialog:
        dialog.open = False
        try:
            page.update()
        except Exception as e:
            print(f"Non-critical error updating page after closing dialog: {e}")

def update_field_border(control: ft.TextField, is_valid: bool, is_empty: bool):
    if is_empty:
        control.border_color = None
    elif is_valid:
        # Using updated ft.Colors
        control.border_color = ft.Colors.GREEN_500
    else:
        # Using updated ft.Colors
        control.border_color = ft.Colors.RED_500

# =======================
# Main View (Transfer Page) - Updated Colors/Icons & Validate Fix
# =======================
def main_view(page: ft.Page):
    global selected_phone

    # --- Controls (Updated ft.Colors / ft.Icons) ---
    phone_number = ft.TextField(
        label=get_text("phone_label"),
        hint_text=get_text("phone_hint"),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        max_length=11,
        # Using updated ft.Icons
        prefix_icon=ft.Icons.PHONE,
        input_filter=ft.InputFilter(regex_string=r'\d'),
        text_align=ft.TextAlign.LEFT
    )

    confirm_phone_number = ft.TextField(
        label=get_text("confirm_phone_label"),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        max_length=11,
        # Using updated ft.Icons
        prefix_icon=ft.Icons.PHONE,
        input_filter=ft.InputFilter(regex_string=r'\d'),
        text_align=ft.TextAlign.LEFT
    )

    amount = ft.TextField(
        label=get_text("amount_label"),
        hint_text=get_text("amount_hint"),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        # Using updated ft.Icons
        prefix_icon=ft.Icons.MONEY,
        input_filter=ft.InputFilter(regex_string=r'\d'),
        text_align=ft.TextAlign.LEFT
    )

    error_text = ft.Text(
        value="",
        # Using updated ft.Colors
        color=ft.Colors.RED_ACCENT_700,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    speech_status_label = ft.Text("", size=12,
                                  # Using updated ft.Colors
                                  color=ft.Colors.GREY_600,
                                  text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT)

    mic_permission_info = ft.Text(
        get_text("mic_permission_note"),
        size=10,
        # Using updated ft.Colors
        color=ft.Colors.GREY_500,
        italic=True,
        text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT
    )

    if selected_phone:
        print(f"Selected phone from contacts: {selected_phone}")
        phone_number.value = selected_phone
        confirm_phone_number.value = selected_phone
        selected_phone = None

    # --- Validation Logic (Fixed page.update() call) ---
    def validate_data(_=None):
        phone_val = phone_number.value or ""
        confirm_val = confirm_phone_number.value or ""
        amount_val = amount.value or ""
        current_error = ""
        is_valid = True

        phone_ok = validate_phone_format(phone_val)
        update_field_border(phone_number, phone_ok, not phone_val)
        if not phone_ok and phone_val:
            current_error = get_text("validation_invalid_phone")
            is_valid = False

        confirm_ok = (phone_val == confirm_val)
        update_field_border(confirm_phone_number, confirm_ok, not confirm_val)
        if not confirm_ok and confirm_val and phone_ok:
            current_error = get_text("validation_mismatch_phone")
            is_valid = False
        elif not confirm_val and phone_ok and phone_val:
             current_error = get_text("validation_confirm_phone_missing")
             is_valid = False

        amount_ok = False
        if amount_val and amount_val.isdigit() and int(amount_val) > 0:
            amount_ok = True
        update_field_border(amount, amount_ok, not amount_val)
        if not amount_ok and amount_val:
            current_error = get_text("validation_invalid_amount")
            is_valid = False
        elif not amount_val and phone_ok and confirm_ok and bool(phone_val) and bool(confirm_val):
             current_error = get_text("validation_amount_missing")
             is_valid = False

        final_valid = phone_ok and confirm_ok and amount_ok and bool(phone_val) and bool(confirm_val) and bool(amount_val)

        if final_valid:
            error_text.value = get_text("validation_ok")
            # Using updated ft.Colors
            error_text.color = ft.Colors.GREEN_700
        elif current_error:
            error_text.value = current_error
            # Using updated ft.Colors
            error_text.color = ft.Colors.RED_ACCENT_700
        elif not phone_val and not confirm_val and not amount_val:
             error_text.value = ""
        elif not final_valid and (phone_val or confirm_val or amount_val):
            error_text.value = get_text("validation_all_fields_missing")
            # Using updated ft.Colors
            error_text.color = ft.Colors.RED_ACCENT_700
        else:
             error_text.value = ""


        call_button.disabled = not final_valid
        try:
            # **** FIX: Use page.update() without arguments ****
            page.update()
        except Exception as e: print(f"Update error in validate_data: {e}")


    # --- Button Actions (No functional changes needed) ---
    def make_call(_):
        phone = phone_number.value
        amt = amount.value
        validate_data()
        if not call_button.disabled:
            dial_code = f"tel:*9*7*{phone}*{amt}%23"
            print(f"Launching USSD code: {dial_code}")
            try:
                page.launch_url(dial_code)
                show_snackbar(page, get_text("sending_snackbar", amount=amt, phone=phone))
            except Exception as ex:
                print(f"Error launching URL: {ex}")
                show_snackbar(page, get_text("launch_url_error", ex=ex), is_error=True)
        else:
            show_snackbar(page, get_text("send_error_snackbar"), is_error=True)

    def update_speech_status_ui(status: str):
        if page:
             page.run_thread_safe(_update_speech_status, status)

    def _update_speech_status(status: str):
        speech_status_label.value = status
        try: page.update([speech_status_label])
        except Exception as e: print(f"Update error in _update_speech_status: {e}")

    def handle_speech_result(digits: str | None, success: bool):
        if page:
            page.run_thread_safe(_handle_speech_result_ui, digits, success)

    def _handle_speech_result_ui(digits: str | None, success: bool):
        voice_button.disabled = False
        if success:
            if digits is not None and digits:
                cleaned_digits = digits
                phone_number.value = cleaned_digits[:11]
                confirm_phone_number.value = cleaned_digits[:11]
                show_snackbar(page, get_text("speech_recognized_number", number=phone_number.value))
                validate_data()
                amount.focus()
            else:
                show_snackbar(page, get_text("speech_no_digits"), is_error=True)
                validate_data()
        elif digits is None and not success:
            validate_data()

        try: page.update([voice_button, phone_number, confirm_phone_number])
        except Exception as e: print(f"Update error in _handle_speech_result_ui: {e}")


    def voice_input_click(e):
        e.control.disabled = True
        phone_number.value = ""
        confirm_phone_number.value = ""
        error_text.value = ""
        update_field_border(phone_number, False, True)
        update_field_border(confirm_phone_number, False, True)
        speech_status_label.value = get_text("recognizing")
        try: page.update()
        except Exception as ex: print(f"Update error in voice_input_click: {ex}")
        recognize_speech_thread(update_speech_status_ui, handle_speech_result)


    def clear_fields(_):
        phone_number.value = ""
        confirm_phone_number.value = ""
        amount.value = ""
        error_text.value = ""
        speech_status_label.value = ""
        update_field_border(phone_number, False, True)
        update_field_border(confirm_phone_number, False, True)
        update_field_border(amount, False, True)
        call_button.disabled = True
        phone_number.focus()
        try: page.update()
        except Exception as e: print(f"Update error in clear_fields: {e}")
        print(get_text("fields_cleared"))


    phone_number.on_change = validate_data
    confirm_phone_number.on_change = validate_data
    amount.on_change = validate_data

    # --- Buttons (Updated ft.Colors / ft.Icons) ---
    call_button = ft.ElevatedButton(
        text=get_text("send_button"),
        disabled=True,
        # Using updated ft.Icons
        icon=ft.Icons.SEND,
        on_click=make_call,
        expand=True,
        style=ft.ButtonStyle(padding=ft.padding.symmetric(vertical=12))
    )
    voice_button = ft.IconButton(
        # Using updated ft.Icons
        icon=ft.Icons.MIC,
        tooltip=get_text("mic_tooltip"),
        on_click=voice_input_click,
        # Using updated ft.Colors
        icon_color=ft.Colors.RED_700,
        icon_size=28
    )
    clear_button = ft.OutlinedButton(
        get_text("clear_button"),
        # Using updated ft.Icons
        icon=ft.Icons.CLEAR_ALL,
        on_click=clear_fields,
        expand=True,
        style=ft.ButtonStyle(padding=ft.padding.symmetric(vertical=12))
    )
    contacts_button = ft.ElevatedButton(
        get_text("contacts_button"),
        # Using updated ft.Icons
        icon=ft.Icons.CONTACTS,
        on_click=lambda _: page.go("/contacts"),
        expand=True,
        style=ft.ButtonStyle(padding=ft.padding.symmetric(vertical=12))
    )

    # --- Build View Content (Updated ft.Colors) ---
    content = ft.Column(
        [
            ft.Text(get_text("main_view_title"), size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Row([phone_number, voice_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row(
                [
                    mic_permission_info,
                    speech_status_label,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            confirm_phone_number,
            amount,
            ft.Container(error_text, alignment=ft.alignment.center, padding=10),
            ft.Row(
                [clear_button, call_button],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=10
            ),
            # Using updated ft.Colors
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row([contacts_button], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    validate_data()

    return ft.View(
        route="/",
        padding=20,
        controls=[
            content
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# =======================
# Contacts View (Updated Colors/Icons & PopupMenuItem Fix)
# =======================
def contacts_view(page: ft.Page):

    _selected_contact_id_for_edit = None
    edit_name_field = ft.TextField(label=get_text("edit_contact_name_label"), expand=True, text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT)
    edit_phone_field = ft.TextField(
        label=get_text("edit_contact_phone_label"),
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=11,
        expand=True,
        input_filter=ft.InputFilter(regex_string=r'\d'),
        text_align=ft.TextAlign.LEFT
    )

    edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(get_text("edit_contact_dialog_title"), text_align=ft.TextAlign.CENTER),
            content=ft.Column([
                edit_name_field,
                edit_phone_field
            ], spacing=15, tight=True, height=150),
            actions=[
                ft.TextButton(
                    get_text("edit_save_button"),
                    # Using updated ft.Icons
                    icon=ft.Icons.SAVE,
                    on_click=lambda _: save_edit()
                ),
                # Using updated ft.Icons
                ft.TextButton(get_text("cancel"), icon=ft.Icons.CANCEL, on_click=lambda _: close_specific_dialog(page, edit_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

    if edit_dialog not in page.overlay:
        page.overlay.append(edit_dialog)
        print("Edit dialog added to overlay.")

    # --- Controls (Updated ft.Icons) ---
    new_name = ft.TextField(label=get_text("add_contact_name_label"), expand=True, text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT)
    new_phone = ft.TextField(
        label=get_text("add_contact_phone_label"),
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=11,
        expand=True,
        input_filter=ft.InputFilter(regex_string=r'\d'),
        # Using updated ft.Icons
        prefix_icon=ft.Icons.PHONE,
        text_align=ft.TextAlign.LEFT
    )

    contacts_list_view = ft.ListView(spacing=5, expand=True, auto_scroll=True)

    search_field = ft.TextField(
        label=get_text("search_placeholder"),
        expand=True,
        # Using updated ft.Icons
        prefix_icon=ft.Icons.SEARCH,
        text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT
    )

    # --- Dialog Save Function (Updated ft.Colors) ---
    def save_edit():
        nonlocal _selected_contact_id_for_edit
        contact_id = _selected_contact_id_for_edit

        if contact_id is None:
            show_snackbar(page, get_text("db_edit_fail_no_id"), is_error=True)
            return

        new_name_val = edit_name_field.value
        new_phone_val = edit_phone_field.value

        if not new_name_val or not new_phone_val:
            show_snackbar(page, get_text("db_update_fail_validation"), is_error=True)
            if not new_name_val: edit_name_field.focus()
            else: edit_phone_field.focus()
            page.update()
            return

        if not validate_phone_format(new_phone_val):
            show_snackbar(page, get_text("db_update_fail_phone_format"), is_error=True)
            # Using updated ft.Colors
            edit_phone_field.border_color = ft.Colors.RED_500
            edit_phone_field.focus()
            page.update()
            return
        else:
             edit_phone_field.border_color = None

        success, message = update_contact_by_id(contact_id, new_name_val, new_phone_val)
        show_snackbar(page, message, is_error=not success)

        if success:
            close_specific_dialog(page, edit_dialog)
            load_contacts_ui(search_field.value)
            _selected_contact_id_for_edit = None
        else:
            # Using updated ft.Colors
            edit_phone_field.border_color = ft.Colors.RED_500 # Show error on field
            edit_phone_field.focus()
            page.update()

    # --- Dialog Open Function (No changes needed) ---
    def open_edit_dialog(cid: int, current_name: str, current_phone: str):
        nonlocal _selected_contact_id_for_edit
        print(f"Opening edit dialog for ID: {cid}, Name: {current_name}")

        _selected_contact_id_for_edit = cid
        edit_name_field.value = current_name
        edit_phone_field.value = current_phone
        edit_phone_field.border_color = None
        edit_dialog.open = True
        try:
            page.update()
            print("Edit dialog opened.")
        except Exception as update_error:
            print(f"Error updating page to show edit dialog: {update_error}")
            show_snackbar(page, get_text("dialog_show_error"), is_error=True)

    # --- Contact Actions (Updated ft.Colors / ft.Icons) ---
    def delete_contact_action(contact_id: int, name_to_delete: str, phone_to_delete: str):
        def confirm_delete(_):
             if page.dialog:
                 close_specific_dialog(page, page.dialog)
             success, message = delete_contact_by_id(contact_id)
             show_snackbar(page, message, is_error=not success)
             if success:
                 load_contacts_ui(search_field.value)

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(get_text("confirm_delete_title"), text_align=ft.TextAlign.CENTER),
            content=ft.Text(get_text("confirm_delete_content", name=name_to_delete, phone=phone_to_delete),
                             text_align=ft.TextAlign.CENTER),
            actions=[
                # Using updated ft.Colors / ft.Icons
                ft.TextButton(get_text("delete"), style=ft.ButtonStyle(color=ft.Colors.RED), icon=ft.Icons.DELETE_FOREVER, on_click=confirm_delete),
                ft.TextButton(get_text("cancel"), icon=ft.Icons.CANCEL, on_click=lambda _: close_specific_dialog(page, page.dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        page.dialog.open = True
        try: page.update()
        except Exception as e: print(f"Error showing delete confirm dialog: {e}")


    def select_contact_action(phone_to_select: str):
        global selected_phone
        selected_phone = phone_to_select
        print(f"Contact selected: {phone_to_select}. Navigating back.")
        page.go("/")

    # --- Load Contacts into UI (Updated Colors/Icons & PopupMenuItem Fix) ---
    def load_contacts_ui(filter_text: str = ""):
        print(f"Loading contacts UI with filter: '{filter_text}'")
        contacts_list_view.controls.clear()
        contacts = fetch_contacts(filter_text.strip())

        if not contacts:
            contacts_list_view.controls.append(
                ft.Container(
                    # Using updated ft.Colors
                    content=ft.Text(get_text("no_contacts"), italic=True, color=ft.Colors.GREY_500),
                    alignment=ft.alignment.center, padding=30
                )
            )
        else:
            for contact_id, name, phone in contacts:
                contact_card = ft.Card(
                    elevation=1.5,
                    margin=ft.margin.symmetric(vertical=3, horizontal=2),
                    content=ft.ListTile(
                        # Using updated ft.Icons / ft.Colors
                        leading=ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.RED_300),
                        title=ft.Text(name, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT),
                        # Using updated ft.Colors and ft.colors.with_opacity
                        subtitle=ft.Text(phone, color=ft.colors.with_opacity(0.7, ft.Colors.ON_SURFACE), text_align=ft.TextAlign.RIGHT if current_lang == 'ar' else ft.TextAlign.LEFT),
                        trailing=ft.PopupMenuButton(
                            # Using updated ft.Icons
                            icon=ft.Icons.MORE_VERT,
                            tooltip=get_text("options_menu_tooltip"),
                            items=[
                                ft.PopupMenuItem(
                                    text=get_text("select_contact_menu"),
                                    # Using updated ft.Icons
                                    icon=ft.Icons.SEND_TO_MOBILE,
                                    on_click=lambda _, p=phone: select_contact_action(p)
                                ),
                                ft.PopupMenuItem(
                                    text=get_text("edit_contact_menu"),
                                    # Using updated ft.Icons
                                    icon=ft.Icons.EDIT_NOTE,
                                    on_click=lambda _, cid=contact_id, n=name, ph=phone: open_edit_dialog(cid, n, ph)
                                ),
                                ft.PopupMenuItem(),
                                # **** FIX: Use content instead of text/text_style ****
                                ft.PopupMenuItem(
                                    # Using updated ft.Icons
                                    icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                                    content=ft.Text(
                                        get_text("delete_contact_menu"),
                                        # Using updated ft.Colors
                                        color=ft.Colors.RED_500
                                    ),
                                    on_click=lambda _, cid=contact_id, n=name, ph=phone: delete_contact_action(cid, n, ph)
                                ),
                            ]
                        ),
                        visual_density=ft.VisualDensity.COMPACT,
                    )
                )
                contacts_list_view.controls.append(contact_card)
        print(f"Loaded {len(contacts)} items into list view.")
        try:
            contacts_list_view.update()
        except Exception as update_error:
            print(f"Error updating contacts list view: {update_error}. Updating page.")
            try: page.update()
            except Exception as page_update_error: print(f"Error updating page after loading contacts: {page_update_error}")

    # --- Add New Contact Action (Updated ft.Colors) ---
    def add_new_contact_click(_):
        name_val = new_name.value.strip()
        phone_val = new_phone.value.strip()

        new_name.border_color = None
        new_phone.border_color = None

        if not name_val:
            show_snackbar(page, get_text("db_add_fail_validation"), is_error=True)
            # Using updated ft.Colors
            new_name.border_color = ft.Colors.RED_500
            new_name.focus()
            page.update()
            return
        if not validate_phone_format(phone_val):
            show_snackbar(page, get_text("db_add_fail_phone_format"), is_error=True)
            # Using updated ft.Colors
            new_phone.border_color = ft.Colors.RED_500
            new_phone.focus()
            page.update()
            return

        success, message = add_contact(name_val, phone_val)
        show_snackbar(page, message, is_error=not success)
        if success:
            new_name.value = ""
            new_phone.value = ""
            new_name.border_color = None
            new_phone.border_color = None
            new_name.focus()
            load_contacts_ui(search_field.value)
            try: page.update()
            except Exception as e: print(f"Update error after adding contact: {e}")
        else:
            # Using updated ft.Colors
            new_phone.border_color = ft.Colors.RED_500
            new_phone.focus()
            page.update()

    # --- Search and Balance Actions (Updated ft.Icons) ---
    def clear_search(_=None):
        search_field.value = ""
        load_contacts_ui()
        search_field.focus()
        try: page.update()
        except Exception as e: print(f"Update error in clear_search: {e}")

    search_field.on_change = lambda e: load_contacts_ui(e.control.value)
    search_field.suffix = ft.IconButton(
        # Using updated ft.Icons
        icon=ft.Icons.CLEAR,
        on_click=clear_search,
        tooltip=get_text("clear_search_tooltip")
    )

    def check_balance(_):
        dial_code = "tel:*9*13%23"
        print("Launching USSD code for balance check.")
        try:
            page.launch_url(dial_code)
            show_snackbar(page, get_text("balance_snackbar"))
        except Exception as ex:
            print(f"Error launching URL: {ex}")
            show_snackbar(page, get_text("launch_url_error", ex=ex), is_error=True)

    # --- Buttons (Updated ft.Icons) ---
    add_button = ft.ElevatedButton(get_text("add_contact_button"), icon=ft.Icons.ADD, on_click=add_new_contact_click, expand=True)
    back_button = ft.OutlinedButton(get_text("back_button"), icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"), expand=True)
    balance_button = ft.OutlinedButton(get_text("balance_button"), icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, on_click=check_balance, expand=True)

    # --- Build View Content (Updated ft.Colors) ---
    content = ft.Column(
        [
            ft.Text(get_text("contacts_view_title"), size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Card(
                elevation=2,
                margin=ft.margin.only(bottom=10),
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text(get_text("add_contact_card_title"), weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        new_name,
                        new_phone,
                        ft.Row([add_button], alignment=ft.MainAxisAlignment.CENTER)
                    ], spacing=10)
                )
            ),
            ft.Divider(height=10),
            ft.Text(get_text("contact_list_title"), size=18, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            search_field,
            ft.Container(
                content=contacts_list_view,
                expand=True,
                # Using updated ft.Colors
                border=ft.border.all(1, ft.Colors.BLACK26),
                border_radius=ft.border_radius.all(5),
                padding=5,
            ),
            ft.Divider(height=10),
            ft.Row(
                [back_button, balance_button],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=10
            )
        ],
        expand=True, spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    load_contacts_ui()

    return ft.View(
        route="/contacts",
        padding=15,
        controls=[
            content
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# =======================
# Main Application Setup (Updated Colors/Icons)
# =======================
def main(page: ft.Page):
    page.title = get_text("app_title")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        # Using updated ft.Colors
        color_scheme_seed=ft.Colors.RED,
        font_family="Roboto"
    )
    page.rtl = (current_lang == "ar")

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_resizable = True
    page.window_width = 420
    page.window_height = 750

    if not os.path.exists(DB_NAME):
         print(f"Database file '{DB_NAME}' not found. Creating...")
    create_db()

    def change_language(_):
        global current_lang
        current_lang = "en" if current_lang == "ar" else "ar"
        page.rtl = (current_lang == "ar")
        current_route = page.route
        # It's necessary to clean the page to correctly rebuild controls with new text/rtl settings
        page.clean()
        print(f"Language changed to {current_lang}. Reloading route: {current_route}")
        # Add a small delay if needed, but usually clean()+go() is enough
        page.go(current_route if current_route else "/")


    def build_app_bar(current_route):
        title_text = ""
        leading_control = None
        if current_route == "/contacts":
            title_text = get_text("contacts_view_appbar_title")
            # Using updated ft.Icons
            leading_control = ft.IconButton(
                 icon=ft.Icons.ARROW_BACK_IOS_NEW if page.platform != ft.PagePlatform.IOS else ft.Icons.ARROW_BACK_Ios,
                 tooltip=get_text("back_button"),
                 on_click=lambda _: page.go("/")
             )
        else:
            title_text = get_text("app_title")

        return ft.AppBar(
                title=ft.Text(title_text, weight=ft.FontWeight.BOLD),
                center_title=True,
                # Using updated ft.Colors
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                leading=leading_control,
                actions=[
                    ft.TextButton(
                        get_text("toggle_language"),
                        # Using updated ft.Icons
                        icon=ft.Icons.LANGUAGE,
                        on_click=change_language,
                        # Using updated ft.Colors
                        style=ft.ButtonStyle(color=ft.Colors.WHITE)
                    ),
                    # Using updated ft.Colors
                    ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT), # Spacer
                ]
            )

    def route_change(route_event: ft.RouteChangeEvent):
        print(f"Route change requested to: {route_event.route}")
        # Ensure page state is fresh before building views
        page.views.clear()
        # Make sure overlay dialogs are cleared on view change if they shouldn't persist
        # page.overlay.clear() # Uncomment if edit dialog should always close on navigation

        current_app_bar = build_app_bar(route_event.route)

        if route_event.route == "/contacts":
            # Rebuild the view every time to ensure language is correct
            contacts_page_view = contacts_view(page)
            contacts_page_view.appbar = current_app_bar
            page.views.append(contacts_page_view)
        else:
            # Rebuild the view every time
            main_page_view = main_view(page)
            main_page_view.appbar = current_app_bar
            page.views.append(main_page_view)

        try:
            page.update()
        except Exception as e:
             print(f"Error updating page on route change: {e}")

    def view_pop(view_event: ft.ViewPopEvent):
        print("View pop requested.")
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
             print("Cannot pop the root view.")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    print(f"Initial route: {page.route}")
    page.go(page.route if page.route else "/")

# =======================
# Run the Application
# =======================
if __name__ == "__main__":
    try:
        # Pass target function as argument to ft.app
        ft.app(target=main)
    except ImportError:
         print("Error: Flet library not found. Please install it using 'pip install flet'")
    except Exception as e:
         print(f"An unexpected error occurred running the app: {e}")
         import traceback
         print(traceback.format_exc()) # Print full traceback for debugging
