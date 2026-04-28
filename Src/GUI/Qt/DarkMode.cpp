#include "DarkMode.h"

#include <QGuiApplication>
#include <QPalette>
#include <QStyleHints>

bool IsDarkModeActive()
{
#if QT_VERSION >= QT_VERSION_CHECK(6, 8, 0)
    Qt::ColorScheme Sheme = QGuiApplication::styleHints()->colorScheme();
    return Sheme == Qt::ColorScheme::Dark;
#else
    return false;
#endif
}

void SetDarkMode(bool par_DarkMode)
{
#if QT_VERSION >= QT_VERSION_CHECK(6, 8, 0)
    if (par_DarkMode) {
        if (!IsDarkModeActive()) {
            QGuiApplication::styleHints()->setColorScheme(Qt::ColorScheme::Dark);
        }
    } else {
        if (IsDarkModeActive()) {
            QGuiApplication::styleHints()->setColorScheme(Qt::ColorScheme::Light);
        }
    }
#endif
}
