#!/bin/bash

# Скрипт для запуска React frontend

echo "⚛️ Запуск Vibe Coding Frontend..."

# Переходим в директорию frontend
cd frontend

# Проверяем, установлен ли Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Пожалуйста, установите Node.js 16+ и попробуйте снова."
    exit 1
fi

# Проверяем, установлен ли npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm не найден. Пожалуйста, установите npm и попробуйте снова."
    exit 1
fi

# Устанавливаем зависимости если node_modules не существует
if [ ! -d "node_modules" ]; then
    echo "📦 Установка зависимостей..."
    npm install
fi

# Запускаем React приложение
echo "🌟 Запуск React приложения..."
npm start

