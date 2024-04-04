
set -e
echo "Linting and fixing js..."
npx eslint src --fix
echo "Linting and fixing css..."
npx stylelint "src/**/*.css" --fix
echo "Linting html..."
./lint_html.sh
