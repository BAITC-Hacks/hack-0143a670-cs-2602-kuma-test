#!/usr/bin/env python3
"""
Классификатор обращений пользователей и генератор черновиков ответов.

Категории:
  - справка: Информационные запросы, получение документов, справки, локации.
  - жалоба: Замечания, претензии, сбои сервисов, очереди.
  - другое: Запись на консультацию, прочие индивидуальные вопросы.
"""

import re
import sys
from pathlib import Path
from typing import Tuple


def classify_and_draft(text: str) -> Tuple[str, str]:
    """
    Определяет категорию обращения и подготавливает черновик ответа на русском языке.
    
    Args:
        text: Текст обращения.
        
    Returns:
        Tuple[str, str]: Кортеж (категория, черновик_ответа).
    """
    text_lower = text.lower()

    # 1. Шаблоны для категории 'жалоба'
    complaint_keywords = [
        r"\bпропал\b", r"\bочередь\b", r"\bхолодн", r"\bне работает\b",
        r"\bсломал", r"\bжалоб", r"\bплохо\b", r"\bошибк", r"\bпроблем"
    ]
    is_complaint = any(re.search(pat, text_lower) for pat in complaint_keywords)

    # 2. Шаблоны для категории 'справка'
    info_keywords = [
        r"\bсправк", r"\bкак получить\b", r"\bгде\b", r"\bрасписание\b",
        r"\bкак найти\b", r"\bинформац", r"\bдокумент"
    ]
    is_info = any(re.search(pat, text_lower) for pat in info_keywords)

    # 3. Шаблоны для категории 'другое' (запись, консультация)
    other_keywords = [
        r"\bзаписаться\b", r"\bзапись\b", r"\bконсультац", r"\bвстреч"
    ]
    is_other = any(re.search(pat, text_lower) for pat in other_keywords)

    # Логика принятия решения
    if is_complaint:
        category = "жалоба"
        if "wi-fi" in text_lower or "вайфай" in text_lower or "интернет" in text_lower:
            draft = (
                "Здравствуйте! Спасибо за сигнал. Информация о проблемах с Wi-Fi в корпусе B "
                "передана в IT-отдел. Специалисты уже занимаются восстановлением доступа."
            )
        elif "столов" in text_lower or "еда" in text_lower or "очередь" in text_lower:
            draft = (
                "Здравствуйте! Нам очень жаль, что вы столкнулись с давкой и холодной едой. "
                "Ваше обращение передано управляющему столовой для проверки оборудования и оптимизации работы касс."
            )
        else:
            draft = (
                "Здравствуйте! Благодарим за обращение. Приносим извинения за доставленные неудобства. "
                "Ваш сигнал принят и передан ответственной службе."
            )

    elif is_info:
        category = "справка"
        if "справк" in text_lower or "учёб" in text_lower:
            draft = (
                "Здравствуйте! Справку о месте учёбы можно заказать в личном кабинете студента "
                "или обратиться в учебный офис (деканат). Срок оформления — от 1 до 3 рабочих дней."
            )
        elif "парковк" in text_lower or "гост" in text_lower:
            draft = (
                "Здравствуйте! Гостевая парковка находится возле северного въезда (КПП №2). "
                "Въезд осуществляется по предварительному согласованию или разовому пропуску."
            )
        else:
            draft = (
                "Здравствуйте! Вся необходимая информация представлена на информационном портале. "
                "Если требуется помощь в поиске, напишите нам подробнее."
            )

    elif is_other:
        category = "другое"
        if "записаться" in text_lower or "консультац" in text_lower:
            draft = (
                "Здравствуйте! Вы можете записаться на консультацию через электронную очередь в личном кабинете "
                "или обратившись к администратору. Уточните, по какому предмету или вопросу требуется консультация?"
            )
        else:
            draft = (
                "Здравствуйте! Ваш запрос принят. Мы уточняем информацию и ответим вам в ближайшее время."
            )

    else:
        category = "другое"
        draft = (
            "Здравствуйте! Благодарим за обращение. Ваше сообщение зарегистрировано и передано специалисту."
        )

    return category, draft


def clean_line(line: str) -> str:
    """Удаляет порядковый номер в начале строки (например, '1) ' или '1. ')."""
    return re.sub(r"^\d+[\)\.]\s*", "", line.strip())


def main():
    script_dir = Path(__file__).parent
    input_file = script_dir / "messages.txt"

    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"Ошибка: Файл '{input_file}' не найден.", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("КЛАССИФИКАЦИЯ ОБРАЩЕНИЙ И ГЕНЕРАЦИЯ ЧЕРНОВИКОВ ОТВЕТОВ")
    print("=" * 80)

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for idx, raw_line in enumerate(lines, 1):
        text = clean_line(raw_line)
        category, draft = classify_and_draft(text)

        print(f"\n[Обращение #{idx}]")
        print(f"Текст:      {text}")
        print(f"Категория:  {category}")
        print(f"Черновик:   {draft}")
        print("-" * 80)


if __name__ == "__main__":
    main()
