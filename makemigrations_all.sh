#!/bin/bash
# makemigrations_all.sh - 모든 앱의 마이그레이션을 한번에 생성

echo "🔍 프로젝트의 모든 Django 앱을 찾는 중..."

# models.py가 있는 디렉토리들을 찾기 (제외 디렉토리 설정)
APPS=$(find . -name "models.py" \
    -not -path "./venv/*" \
    -not -path "./.venv/*" \
    -not -path "./env/*" \
    -not -path "./config/*" \
    -not -path "./.git/*" \
    | xargs dirname \
    | sed 's|^\./||' \
    | sort | uniq)

if [ -z "$APPS" ]; then
    echo "❌ Django 앱이 발견되지 않았습니다."
    exit 1
fi

# 앱 목록을 한줄로 만들기
APP_LIST=""
echo "📱 발견된 앱들:"
for app in $APPS; do
    echo "  - $app"
    APP_LIST="$APP_LIST $app"
done

echo ""
echo "🚀 makemigrations 실행 중..."
echo "실행 명령어: python manage.py makemigrations$APP_LIST"

# 모든 앱을 한번에 전달
python manage.py makemigrations $APP_LIST

if [ $? -eq 0 ]; then
    echo "✅ 모든 앱의 마이그레이션이 성공적으로 생성되었습니다!"
else
    echo "❌ 마이그레이션 생성 중 오류가 발생했습니다."
    exit 1
fi