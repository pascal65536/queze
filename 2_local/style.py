style_sheet = """
        QTabBar::tab {
            width: 100px;
        }

        QTabBar::tab {
            font-weight: bold; /* Сделать текст жирным (опционально) */
        }  

        /* Подчеркивание текста второй вкладки */
        QTabBar::tab:nth-child(2) {
            text-decoration: underline; /* Подчеркнуть текст */
        }      
        """
