import re
import os
import PyPDF2
import argparse

def extract_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Ошибка чтения {pdf_path}: {str(e)}")
    return text

def find_inn(text):
    # Ищем все ИНН, но исключаем 1430001231
    inns = re.findall(r'\b\d{10}\b|\b\d{12}\b', text)
    valid_inns = [inn for inn in inns if inn != "для_исключения_1430001231"]
    return valid_inns[0] if valid_inns else None

def process_file(file_path):
    print(f"Обработка: {file_path}")
    text = extract_text(file_path)
    if not text:
        return
    
    inn = find_inn(text)
    if inn:
        new_name = f"{os.path.splitext(file_path)[0]}_ИНН{inn}.pdf"
        os.rename(file_path, new_name)
        print(f"Переименован: {os.path.basename(new_name)}")
    else:
        print("ИНН не найден (либо найден только исключённый _________)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Путь к PDF или папке")
    args = parser.parse_args()

    path = args.path
    if os.path.isfile(path) and path.lower().endswith('.pdf'):
        process_file(path)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            if f.lower().endswith('.pdf'):
                process_file(os.path.join(path, f))
    else:
        print("Неверный путь. Укажите файл PDF или папку")

if __name__ == "__main__":
    main()