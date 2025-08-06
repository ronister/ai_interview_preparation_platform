### DIRECTORY PROJECT_ROOT FOLDER STRUCTURE ###
ai_interview_preparation_platform/
    .env.example
    .gitignore
    README.md
    babel.config.js
    db.sqlite3
    manage.py
    package.json
    pnpm-lock.yaml
    poetry.lock
    postcss.config.cjs
    prettier.config.mjs
    pyproject.toml
    run.sh
    tsconfig.json
    webpack-stats.json
    webpack.config.js
    yarn.lock
    ai_interview_preparation_platform/
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
    assets/
        js/
            App.tsx
            index.jsx
            utils/
                djangoAIAssistantAuth.ts
                networkLogger.ts
                pythonRunner.ts
            contexts/
                AuthContext.tsx
            components/
                index.ts
                Practice/
                    LevelSuggestionModal.tsx
                    OutputPanel.tsx
                    Practice.module.css
                    PracticeScreen.tsx
                    PythonEditor.tsx
                    QuestionDisplay.tsx
                    UserStats.tsx
                    index.ts
                Auth/
                    ForgotPassword.tsx
                    Login.tsx
                    PrivateRoute.tsx
                    Register.tsx
                Chat/
                    Chat.module.css
                    Chat.tsx
                PracticeScreen/
                    PracticeScreen.tsx
                ThreadsNav/
                    ThreadsNav.module.css
                    ThreadsNav.tsx
            types/
                css.d.ts
        css/
            htmx_index.css
    call_graph/
    apps/
        __init__.py
        practice/
            __init__.py
            admin.py
            apps.py
            grading.py
            grading_criteria.txt
            models.py
            serializers.py
            tests.py
            urls.py
            views.py
        authentication/
            __init__.py
            admin.py
            apps.py
            authentication.py
            middleware.py
            models.py
            permissions.py
            serializers.py
            tests.py
            urls.py
            views.py
        instructions_difficulty_eval/
            __init__.py
            apps.py
            data_processor.py
            difficulty_evaluator.py
            difficulty_service.py
            instructions_difficulty_eval.py
            models.py
            management/
                __init__.py
                commands/
                    __init__.py
                    evaluate_difficulty.py
        rag/
            __init__.py
            admin.py
            ai_assistants.py
            apps.py
            models.py
            management/
                __init__.py
                commands/
                    __init__.py
                    fetch_django_docs.py
        api/
            __init__.py
            admin.py
            apps.py
            claude_service.py
            models.py
            tests.py
            views.py
        demo/
            __init__.py
            apps.py
            middleware.py
            urls.py
            views.py
            templatetags/
                __init__.py
                markdown.py
            templates/
                base.html
                demo/
                    chat_home.html
                    chat_thread.html
                    htmx_index.html
                    react_index.html
    qa/
        apps_practice_views_msb_temp.py
        bugs/
            .gitkeep
        template/
            bug_report.md
    planning/
        process_flow.mermaid
    tests/
        test_db_connection.py
        test_grading_changes.py
        test_grading_details.py
        test_sample_data.py
    operations/
        git/
            reconcile_branches_config.sh
            set_git_email_and_user.sh
            set_git_remote.sh
### DIRECTORY /home/ubuntu_user/main/repositories/ai_interview_preparation_platform FOLDER STRUCTURE ###

### DIRECTORY PROJECT_ROOT FLATTENED CONTENT ###
### webpack.config.js BEGIN ###
const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: "./assets/js/index",
  output: {
    path: path.resolve(__dirname, "assets/webpack_bundles/"),
    // Cannot use publicPath: "auto" here because we need to specify the full URL,
    // since we're serving the files with the Webpack devServer:
    publicPath: "http://localhost:3000/webpack_bundles/",
    filename: "[name]-[contenthash].js",
  },
  devtool: "source-map",
  devServer: {
    hot: true,
    historyApiFallback: true,
    host: "localhost",
    port: 3000,
    // Allow CORS requests from the Django dev server domain:
    headers: { "Access-Control-Allow-Origin": "*" },
  },

  plugins: [
    new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
    new MiniCssExtractPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.(js|jsx|tsx|ts)$/i,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              modules: {
                auto: true, // must be true for Mantine, as it uses both CSS modules and global CSS
                namedExport: false,
              },
              importLoaders: 1, // 1 => postcss-loader
            },
          },
          "postcss-loader",
        ],
      },
    ],
  },

  resolve: {
    extensions: [".js", ".ts", ".jsx", ".tsx"],
    alias: {
      "@": path.resolve(__dirname, "assets/js"),
      // Necessary to deduplicate React due to pnpm link:
      react: path.resolve("./node_modules/react"),
    },
  },
};

### webpack.config.js END ###

### postcss.config.cjs BEGIN ###
module.exports = {
  plugins: {
    "postcss-preset-mantine": {},
    "postcss-simple-vars": {
      variables: {
        "mantine-breakpoint-xs": "36em",
        "mantine-breakpoint-sm": "48em",
        "mantine-breakpoint-md": "62em",
        "mantine-breakpoint-lg": "75em",
        "mantine-breakpoint-xl": "88em",
      },
    },
  },
};

### postcss.config.cjs END ###

### .env.example BEGIN ###
OPENAI_API_KEY=your-key-here
WEATHER_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
FIRECRAWL_API_KEY=your-key-here
LANGCHAIN_API_KEY=your-key-here
LANGCHAIN_TRACING_V2=True

### .env.example END ###

### db.sqlite3 BEGIN ###

### db.sqlite3 END ###

### package.json BEGIN ###
{
  "name": "django-ai-assistant-demo-frontend",
  "version": "0.0.1",
  "private": true,
  "description": "django-ai-assistant demo frontend.",
  "engines": {
    "node": ">=20 <21"
  },
  "scripts": {
    "start": "webpack serve --mode=development --hot"
  },
  "browserslist": [
    "defaults"
  ],
  "main": "js/index.tsx",
  "devDependencies": {
    "@babel/core": "^7.26.10",
    "@babel/preset-env": "^7.26.9",
    "@babel/preset-react": "^7.26.3",
    "@babel/preset-typescript": "^7.27.0",
    "@types/cookie": "^0.6.0",
    "@types/react": "^18.3.20",
    "babel-loader": "^9.2.1",
    "css-loader": "^7.1.2",
    "mini-css-extract-plugin": "^2.9.2",
    "postcss": "^8.5.3",
    "postcss-import": "^16.1.0",
    "postcss-loader": "^8.1.1",
    "postcss-preset-env": "^9.6.0",
    "postcss-preset-mantine": "^1.17.0",
    "postcss-simple-vars": "^7.0.1",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "style-loader": "^4.0.0",
    "typescript": "^5.8.3",
    "webpack": "^5.99.5",
    "webpack-bundle-tracker": "^3.1.1",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^5.2.1"
  },
  "dependencies": {
    "@mantine/core": "^7.17.4",
    "@mantine/form": "^8.1.1",
    "@mantine/hooks": "^7.17.4",
    "@mantine/notifications": "^7.17.4",
    "@tabler/icons-react": "^3.31.0",
    "ace-builds": "^1.32.0",
    "cookie": "^0.6.0",
    "django-ai-assistant-client": "0.1.1",
    "modern-normalize": "^2.0.0",
    "react-ace": "^10.1.0",
    "react-markdown": "^9.1.0",
    "react-router-dom": "^6.30.0"
  }
}

### package.json END ###

### babel.config.js BEGIN ###
"use strict";

module.exports = {
  presets: [
    ["@babel/preset-env", { targets: { node: "current" } }],
    ["@babel/preset-react", { runtime: "automatic" }],
    "@babel/preset-typescript",
  ],
};

### babel.config.js END ###

### pyproject.toml BEGIN ###
[project]
name = "ai-interview-preparation-platform"
version = "0.1.0"
description = ""
authors = [
    {name = "Roni Shternberg"}
]
readme = "README.md"
requires-python = ">=3.12,<4.0"
dependencies = [
    "django (>=5.2.1,<6.0.0)",
    "psycopg2-binary (>=2.9.10,<3.0.0)",
    "python-dotenv (>=1.1.0,<2.0.0)",
    "pandas (>=2.2.3,<3.0.0)",
    "anthropic (>=0.40.0,<1.0.0)",
    "langchain (>=0.3.25,<0.4.0)",
    "tqdm (>=4.67.1,<5.0.0)",
    "django-ai-assistant (>=0.1.2,<0.2.0)",
    "gitpython (>=3.1.44,<4.0.0)",
    "langchain-community (>=0.3.25,<0.4.0)",
    "django-webpack-loader (>=3.2.1,<4.0.0)",
    "pycmarkgfm (>=1.2.1,<2.0.0)",
    "scikit-learn (>=1.7.0,<2.0.0)",
    "djangorestframework (>=3.16.0,<4.0.0)",
    "djangorestframework-simplejwt (>=5.5.0,<6.0.0)",
    "django-cors-headers (>=4.7.0,<5.0.0)",
    "microsandbox (>=0.1.8,<0.2.0)",
    "matplotlib (>=3.10.3,<4.0.0)"
]


[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

### pyproject.toml END ###

### README.md BEGIN ###
# Adaptive Python Interview Preparation Platform using AI Agents  (🚀)

✨ Key Features
* Smart Question Engine – serves problems that match your skill in real time

* Auto-grader – runs code in a sandbox, scores correctness + complexity

* AI Tutor – chat agent offers hints and walkthroughs

* Progress Stats – track accuracy and topic mastery

Open http://localhost:5173 and start practicing!

📂 Project Structure
ai_interview_preparation_platform/
├─ app/
│  ├─ api/               # FastAPI routes
│  ├─ agents/            # LangChain agent definitions
│  ├─ core/              # settings, logging, utilities
│  ├─ grading/           # code analysis & scoring
│  ├─ models/            # SQLAlchemy ORM + pgvector
│  └─ worker.py          # Celery entrypoint
├─ docker/
│  └─ runner/            # minimal image for code execution
├─ frontend/             # React/Tailwind web client
├─ scripts/              # maintenance & seed helpers
└─ tests/                # pytest + coverage

Tech
Django • LangChain • React + TypeScript + Vite • PostgreSQL

📧 Contact
Project Lead: Roni Shternberg
GitHub: @ronister · Email: roni.shternberg@gmail.com
    - Happy coding & good luck with your next Python interview!
### README.md END ###

### manage.py BEGIN ###
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

### manage.py END ###

### tsconfig.json BEGIN ###
{
  "compilerOptions": {
    "target": "ES2021",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "baseUrl": "./",
    "esModuleInterop": true,
    "incremental": true,
    "jsx": "react-jsx",
    "module": "esnext",
    "moduleResolution": "node",
    "noEmit": true,
    "paths": {
      "@/*": ["./assets/js/*"]
    },
    "skipLibCheck": true,
    "strict": true,
    "types": ["node"]
  },
  "include": ["**/*.ts", "**/*.mts", "**/*.tsx"],
  "exclude": ["node_modules"]
}

### tsconfig.json END ###

### .gitignore BEGIN ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
###env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the enitre vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

### Ignore only the file, keep other things in env/
#env/.env

env/*
!env/.env.example

logs/*
!logs/.gitkeep

node_modules/
webpack-stats.json
### .gitignore END ###

### prettier.config.mjs BEGIN ###
/** @type {import("prettier").Config} */

const config = {
  trailingComma: "all",
  tabWidth: 2,
  semi: true,
  singleQuote: false,
  printWidth: 100,
};

export default config;

### prettier.config.mjs END ###

### run.sh BEGIN ###
#!/bin/bash

# Set the execution environment flag
IS_EXECUTION_ENVIRONMENT=false

if [ "$IS_EXECUTION_ENVIRONMENT" = true ]; then
    echo "Running in execution environment mode..."
    msb server start --dev
else
    echo "Running in development mode..."
    
    # Run Django server in background
    echo "Starting Django server..."
    python manage.py runserver &
    DJANGO_PID=$!
    
    # Run yarn start
    echo "Starting yarn..."
    yarn start &
    YARN_PID=$!
    
    # Function to handle cleanup on script exit
    cleanup() {
        echo "Shutting down servers..."
        kill $DJANGO_PID 2>/dev/null
        kill $YARN_PID 2>/dev/null
        exit
    }
    
    # Set up trap to catch interrupts and perform cleanup
    trap cleanup INT TERM
    
    # Wait for both processes
    wait $DJANGO_PID $YARN_PID
fi

### run.sh END ###

### ai_interview_preparation_platform/asgi.py BEGIN ###
"""
ASGI config for ai_interview_preparation_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')

application = get_asgi_application()

### ai_interview_preparation_platform/asgi.py END ###

### ai_interview_preparation_platform/wsgi.py BEGIN ###
"""
WSGI config for ai_interview_preparation_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')

application = get_wsgi_application()

### ai_interview_preparation_platform/wsgi.py END ###

### ai_interview_preparation_platform/urls.py BEGIN ###
"""
URL configuration for ai_interview_preparation_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

# For API endpoints, we'll use csrf_exempt since authentication is handled by JWT
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/practice/", include("apps.practice.urls")),
    path("", include("apps.demo.urls")),
]
### ai_interview_preparation_platform/urls.py END ###

### ai_interview_preparation_platform/__init__.py BEGIN ###

### ai_interview_preparation_platform/__init__.py END ###

### ai_interview_preparation_platform/settings.py BEGIN ###
"""
Django settings for ai_interview_preparation_platform project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR now equals the repository root, two levels up from settings.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Point to env/.env instead of a root-level file
load_dotenv(BASE_DIR / "env" / ".env") 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$9k6)ollzx$#n1ww0^ivae6*ct5&y+qxlhb*_*zpd7oz0c9d)('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "webpack_loader",
    'django_ai_assistant',
    "apps.demo",  # contains the views for the demo app
    'apps.api',  # Generic API services
    'apps.instructions_difficulty_eval',
    'apps.rag',
    'apps.authentication',  # New authentication app
    'apps.practice',  # Practice app for coding interview
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # Add token blacklist
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
    'django.middleware.common.CommonMiddleware',
    'apps.authentication.middleware.DisableCSRFForAPIMiddleware',  # Disable CSRF for API
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.demo.middleware.DjangoAIAssistantAuthMiddleware',  # Add custom middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_interview_preparation_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_interview_preparation_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.getenv("POSTGRES_DB"),
        "USER":     os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST":     os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT":     os.getenv("POSTGRES_PORT", "5432"),
        "OPTIONS":  {"connect_timeout": 10},
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = (BASE_DIR / "assets",)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Delete existing debug.log file and create a fresh one each run
DEBUG_LOG_FILE = LOGS_DIR / "debug.log"
DEBUG_LOG_FILE.unlink(missing_ok=True)  # Delete the file if it exists

# Delete existing grading.log file and create a fresh one each run
GRADING_LOG_FILE = LOGS_DIR / "grading.log"
GRADING_LOG_FILE.unlink(missing_ok=True)  # Delete the file if it exists

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'console_format': {
            'format': '[{levelname}] {asctime} - {name}: {message}',
            'style': '{',
        },
        'grading_format': {
            'format': '{asctime} | {levelname} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_format',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILE,
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'grading_file': {
            'class': 'logging.FileHandler',
            'filename': GRADING_LOG_FILE,
            'formatter': 'grading_format',
            'level': 'DEBUG',
            'mode': 'w',  # Write mode to start fresh each run
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'ai_interview_preparation_platform': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'grading_logger': {
            'handlers': ['grading_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

DJANGO_DOCS_BRANCH = "stable/5.0.x"

# django-webpack-loader

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "webpack_bundles/",
        "CACHE": not DEBUG,
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.authentication.authentication.JWTOnlyAuthentication',  # Use JWT-only for API endpoints
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

# CORS settings - allow your frontend during development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF settings for API
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Django AI Assistant settings
DJANGO_AI_ASSISTANT = {
    'AUTHENTICATION_CLASSES': [
        'apps.authentication.authentication.HybridAuthentication',
    ],
    'PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Authentication settings
LOGIN_URL = '/login'  # Redirect to React login page instead of /accounts/login/
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Session and CSRF cookie settings
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Must be False to allow JavaScript access

### ai_interview_preparation_platform/settings.py END ###

### assets/js/index.jsx BEGIN ###
import React from "react";
import { createRoot } from "react-dom/client";

import App from "./App";

const container = document.getElementById("react-app");
const root = createRoot(container);
root.render(<App />);

### assets/js/index.jsx END ###

### assets/js/App.tsx BEGIN ###
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import React, { useEffect, useState } from "react";
import {
  Container,
  createTheme,
  List,
  MantineProvider,
  rem,
  ThemeIcon,
  Title,
  Button,
  Group,
} from "@mantine/core";
import { Notifications, notifications } from "@mantine/notifications";
import {
  IconChecklist,
  IconBrandDjango,
  IconXboxX,
  IconBubble,
  IconLogout,
  IconUser,
} from "@tabler/icons-react";
import { Chat, PracticeScreen } from "@/components";
import { createBrowserRouter, Link, RouterProvider, useNavigate } from "react-router-dom";
import {
  configAIAssistant,
  useAssistantList,
} from "django-ai-assistant-client";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Login } from "./components/Auth/Login";
import { Register } from "./components/Auth/Register";
import { ForgotPassword } from "./components/Auth/ForgotPassword";
import { PrivateRoute } from "./components/Auth/PrivateRoute";
import { setupNetworkLogging } from "./utils/networkLogger";
import { setupDjangoAIAssistantAuth } from "./utils/djangoAIAssistantAuth";

// Setup auth override immediately before any components load
// This ensures we catch the django-ai-assistant-client's fetch before it's used
setupDjangoAIAssistantAuth(null); // Initial setup without token
setupNetworkLogging();

const theme = createTheme({});

// Configure AI Assistant with authentication - Must run inside AuthProvider
const ConfigureAIAssistant = () => {
  const { accessToken } = useAuth();
  const lastConfiguredTokenRef = React.useRef<string | null>(null);

  useEffect(() => {
    // Skip if we've already configured with this token
    if (accessToken === lastConfiguredTokenRef.current) {
      return;
    }

    console.log('[ConfigureAIAssistant] Updating with token:', {
      hasToken: !!accessToken,
      tokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null
    });
    
    // Update the auth override with the actual token
    setupDjangoAIAssistantAuth(accessToken);
    
    // Also configure via the official API (in case it works)
    const config = { 
      BASE: "ai-assistant",
      HEADERS: accessToken ? {
        'Authorization': `Bearer ${accessToken}`
      } : {}
    };
    
    console.log('[ConfigureAIAssistant] Configuration:', {
      BASE: config.BASE,
      hasAuthHeader: !!config.HEADERS?.Authorization
    });
    
    configAIAssistant(config);
    
    // Remember the last configured token
    lastConfiguredTokenRef.current = accessToken;
  }, [accessToken]);

  return null;
};

const PageWrapper = ({ children }: { children: React.ReactNode }) => {
  // This component allows to use react-router-dom's Link component
  // in the children components.
  return (
    <>
      <Notifications position="top-right" />
      {children}
    </>
  );
};

const ExampleIndex = () => {
  const { user, logout, isAuthenticated, accessToken } = useAuth();
  const navigate = useNavigate();

  // Ensure we have the latest auth state when component mounts
  useEffect(() => {
    console.log('[ExampleIndex] Component mounted, current auth state:', {
      isAuthenticated,
      username: user?.username,
      hasAccessToken: !!accessToken,
      timestamp: new Date().toISOString()
    });
    
    // Check what's in localStorage vs what's in state
    const storedToken = localStorage.getItem('accessToken');
    console.log('[ExampleIndex] Mount - State vs Storage comparison:', {
      stateUsername: user?.username,
      stateToken: accessToken ? `${accessToken.substring(0, 20)}...` : null,
      storageToken: storedToken ? `${storedToken.substring(0, 20)}...` : null,
      tokensMatch: accessToken === storedToken
    });
  }, []); // Only run once on mount

  const handleHTMXClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    
    console.log('[ExampleIndex] HTMX link clicked', {
      currentUser: user?.username,
      isAuthenticated,
      hasAccessToken: !!accessToken,
      timestamp: new Date().toISOString()
    });
    
    if (!isAuthenticated) {
      // If not authenticated, redirect to login
      console.log('[ExampleIndex] Not authenticated, redirecting to login');
      navigate('/login?next=/htmx/');
      return;
    }
    
    try {
      console.log('[ExampleIndex] Creating session for HTMX demo');
      
      // Create a session from JWT token
      const response = await fetch('/create-session/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies to set session
      });
      
      const result = await response.json();
      
      if (result.success) {
        console.log('[ExampleIndex] Session created successfully, navigating to HTMX demo');
        // Navigate to HTMX demo page
        window.location.href = '/htmx/';
      } else {
        console.error('[ExampleIndex] Failed to create session:', result.message);
        navigate('/login?next=/htmx/');
      }
    } catch (error) {
      console.error('[ExampleIndex] Error creating session:', error);
      navigate('/login?next=/htmx/');
    }
  };

  const handleClearProgress = () => {
    const confirmed = window.confirm(`Are you sure you want to clear all progress of ${user?.username}?`);
    
    if (confirmed) {
      clearUserProgress();
    }
  };

  const clearUserProgress = async () => {
    try {
              console.log('[ExampleIndex] Clearing progress for user:', user?.username);
        const response = await (window as any).authenticatedFetch('/api/practice/clear-progress/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      
      if (response.ok) {
        console.log('[ExampleIndex] Progress cleared successfully');
        notifications.show({
          title: 'Success',
          message: 'Clear Progress completed',
          color: 'green',
        });
      } else {
        console.error('[ExampleIndex] Failed to clear progress, response:', response.status);
        const errorData = await response.json().catch(() => ({}));
        notifications.show({
          title: 'Error',
          message: errorData.message || 'Failed to clear progress. Please try again.',
          color: 'red',
        });
      }
    } catch (error) {
      console.error('[ExampleIndex] Error clearing progress:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to clear progress. Please try again.',
        color: 'red',
      });
    }
  };

  return (
    <Container>
      <Group justify="apart" mb="xl">
        <Title order={2} my="md">
          Adaptive Python Interview Preparation Platform Using AI Agents
        </Title>
        {isAuthenticated && (
          <Group>
            <Button
              variant="subtle"
              leftSection={<IconUser size={16} />}
              // onClick={() => navigate('/profile')}
            >
              {user?.username}
            </Button>
            <Button
              variant="light"
              color="orange"
              onClick={handleClearProgress}
            >
              Clear User Progress
            </Button>
            <Button
              variant="light"
              color="red"
              leftSection={<IconLogout size={16} />}
              style={{
                border: 'none',
                '&:hover': {
                  backgroundColor: 'var(--mantine-color-red-7)',
                }
              }}
              onClick={logout}
            >
              Logout
            </Button>
          </Group>
        )}
      </Group>

      <List spacing="sm" size="md" center>
        <List.Item
          icon={
            <ThemeIcon color="teal" size={28} radius="xl">
              <IconChecklist style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
        >
          <Link to="/practice">Python Coding Practice</Link>
        </List.Item>
        <List.Item
          icon={
            <ThemeIcon color="blue" size={28} radius="xl">
              <IconBrandDjango style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
          style={{ display: 'none' }}
        >
          <Link to="/rag-chat">Django Docs RAG Chat</Link>
        </List.Item>
        <List.Item
          icon={
            <ThemeIcon color="blue" size={28} radius="xl">
              <IconBubble style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
        >
          <a href="/htmx/" onClick={handleHTMXClick}>Chat Threads</a>
        </List.Item>
      </List>
    </Container>
  );
};

const Redirect = ({ to }: { to: string }) => {
  window.location.href = to;
  return null;
};

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <ExampleIndex />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/login",
    element: (
      <PageWrapper>
        <Login />
      </PageWrapper>
    ),
  },
  {
    path: "/register",
    element: (
      <PageWrapper>
        <Register />
      </PageWrapper>
    ),
  },
  {
    path: "/forgot-password",
    element: (
      <PageWrapper>
        <ForgotPassword />
      </PageWrapper>
    ),
  },
  {
    path: "/practice",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <PracticeScreen />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/rag-chat",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <Chat assistantId="django_docs_assistant" />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/admin",
    element: (
      <PageWrapper>
        <Redirect to="/admin/" />
      </PageWrapper>
    ),
  },
]);

const App = () => {
  return (
    <MantineProvider theme={theme}>
      <AuthProvider>
        <ConfigureAIAssistant />
        <RouterProvider router={router} />
      </AuthProvider>
    </MantineProvider>
  );
};

export default App;

### assets/js/App.tsx END ###

### assets/js/utils/networkLogger.ts BEGIN ###
// Network request logger to help debug authentication issues

export function setupNetworkLogging() {
  const originalFetch = window.fetch;
  
  window.fetch = async function(...args) {
    const [url, options = {}] = args;
    
    console.log('[NetworkLogger] Fetch request:', {
      url,
      method: options.method || 'GET',
      headers: options.headers,
      hasAuthHeader: !!(options.headers as any)?.['Authorization'],
      authHeaderPreview: (options.headers as any)?.['Authorization'] 
        ? `${(options.headers as any)['Authorization'].substring(0, 30)}...` 
        : null
    });
    
    try {
      const response = await originalFetch.apply(this, args);
      
      console.log('[NetworkLogger] Response:', {
        url,
        status: response.status,
        statusText: response.statusText,
        headers: {
          contentType: response.headers.get('content-type'),
          wwwAuthenticate: response.headers.get('www-authenticate')
        }
      });
      
      // Clone response to read error details for 401s
      if (response.status === 401) {
        const clonedResponse = response.clone();
        try {
          const errorData = await clonedResponse.json();
          console.log('[NetworkLogger] 401 Error details:', errorData);
        } catch (e) {
          console.log('[NetworkLogger] Could not parse 401 error response as JSON');
        }
      }
      
      return response;
    } catch (error) {
      console.error('[NetworkLogger] Fetch error:', {
        url,
        error: error instanceof Error ? error.message : error
      });
      throw error;
    }
  };
  
  console.log('[NetworkLogger] Network logging enabled');
} 
### assets/js/utils/networkLogger.ts END ###

### assets/js/utils/djangoAIAssistantAuth.ts BEGIN ###
// Override django-ai-assistant-client's fetch and XMLHttpRequest to include authentication
export function setupDjangoAIAssistantAuth(accessToken: string | null) {
  console.log('[DjangoAIAssistantAuth] Setting up with token:', {
    hasToken: !!accessToken,
    tokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null
  });

  // Store the original implementations
  const originalFetch = window.fetch;
  const OriginalXHR = window.XMLHttpRequest;

  // Override fetch
  window.fetch = async function(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
    const url = typeof input === 'string' ? input : input instanceof Request ? input.url : input.toString();
    
    // Check if this is an AI assistant endpoint
    if (url.includes('/ai-assistant/')) {
      // Use authenticatedFetch if available (from AuthContext)
      if ((window as any).authenticatedFetch) {
        console.log('[DjangoAIAssistantAuth] Using authenticatedFetch for AI assistant request');
        return (window as any).authenticatedFetch(url, init);
      }
      
      console.log('[DjangoAIAssistantAuth] Intercepting AI assistant fetch request:', {
        url,
        method: init?.method || 'GET',
        hasToken: !!accessToken,
        originalHeaders: init?.headers
      });
      
      // Ensure credentials are included for session auth
      init = init || {};
      init.credentials = 'include'; // This ensures cookies are sent
      
      // Get the latest token from localStorage
      const currentToken = localStorage.getItem('accessToken') || accessToken;
      
      // Add auth header if we have a token
      if (currentToken) {
        init.headers = {
          ...init.headers,
          'Authorization': `Bearer ${currentToken}`,
          'Content-Type': 'application/json',
        };
        
        console.log('[DjangoAIAssistantAuth] Added auth header to fetch request');
      }
      
      console.log('[DjangoAIAssistantAuth] Final fetch request init:', {
        credentials: init.credentials,
        hasAuthHeader: !!(init.headers as any)?.['Authorization']
      });
    }
    
    const response = await originalFetch(input, init);
    
    if (url.includes('/ai-assistant/')) {
      console.log('[DjangoAIAssistantAuth] Fetch response:', {
        url,
        status: response.status,
        statusText: response.statusText
      });
      
      if (response.status === 401) {
        console.error('[DjangoAIAssistantAuth] 401 Unauthorized - Token may be invalid or missing');
        // Log response headers for debugging
        console.log('[DjangoAIAssistantAuth] Response headers:', {
          'www-authenticate': response.headers.get('www-authenticate'),
          'content-type': response.headers.get('content-type')
        });
      }
    }
    
    return response;
  };

  // Override XMLHttpRequest
  window.XMLHttpRequest = class extends OriginalXHR {
    private _url?: string;
    private _method?: string;

    open(method: string, url: string | URL, async?: boolean, username?: string | null, password?: string | null): void {
      this._method = method;
      this._url = url.toString();
      
      if (this._url.includes('/ai-assistant/')) {
        console.log('[DjangoAIAssistantAuth] Intercepting AI assistant XHR request:', {
          url: this._url,
          method: this._method,
          hasToken: !!accessToken
        });
      }
      
      super.open(method, url, async !== false, username, password);
    }

    setRequestHeader(name: string, value: string): void {
      // Let the original header be set first
      super.setRequestHeader(name, value);
      
      // Get the latest token from localStorage
      const currentToken = localStorage.getItem('accessToken') || accessToken;
      
      // If this is an AI assistant request and we haven't set auth yet
      if (this._url?.includes('/ai-assistant/') && currentToken && name.toLowerCase() !== 'authorization') {
        console.log('[DjangoAIAssistantAuth] Setting auth header on XHR');
        super.setRequestHeader('Authorization', `Bearer ${currentToken}`);
      }
    }

    send(body?: Document | XMLHttpRequestBodyInit | null): void {
      if (this._url?.includes('/ai-assistant/')) {
        // Ensure credentials are included
        this.withCredentials = true;
        
        // Get the latest token from localStorage
        const currentToken = localStorage.getItem('accessToken') || accessToken;
        
        // Add auth header if not already set
        if (currentToken) {
          try {
            super.setRequestHeader('Authorization', `Bearer ${currentToken}`);
            console.log('[DjangoAIAssistantAuth] Added auth header to XHR request');
          } catch (e) {
            // Header may have already been set
          }
        }
        
        // Add response listener
        this.addEventListener('load', () => {
          console.log('[DjangoAIAssistantAuth] XHR response:', {
            url: this._url,
            status: this.status,
            statusText: this.statusText
          });
          
          if (this.status === 401) {
            console.error('[DjangoAIAssistantAuth] XHR 401 Unauthorized');
          }
        });
      }
      
      super.send(body);
    }
  } as any;
  
  console.log('[DjangoAIAssistantAuth] Fetch and XHR overrides installed');
} 
### assets/js/utils/djangoAIAssistantAuth.ts END ###

### assets/js/utils/pythonRunner.ts BEGIN ###
// Backend Python execution - no browser-side interpreter needed

// Backend Python execution using Django API
export async function runPythonCode(code: string): Promise<{ output: string; error: string | null }> {
  console.log('Executing Python code on backend:', code.substring(0, 100) + '...');
  
  try {
    // Use the global authenticatedFetch which handles token refresh automatically
    const authenticatedFetch = (window as any).authenticatedFetch;
    
    if (!authenticatedFetch) {
      return {
        output: '',
        error: 'Authentication not available. Please refresh the page.'
      };
    }
    
    const response = await authenticatedFetch('/api/practice/run-python/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code })
    });
    
    if (!response.ok) {
      if (response.status === 408) {
        return {
          output: '',
          error: 'Code execution timed out (10 seconds limit)'
        };
      } else {
        const errorData = await response.json().catch(() => ({}));
        return {
          output: '',
          error: errorData.error || `Server error: ${response.status}`
        };
      }
    }
    
    const result = await response.json();
    console.log('Backend execution result:', result);
    
    return {
      output: result.output || '',
      error: result.error || null
    };
    
  } catch (error) {
    console.error('Backend execution error:', error);
    return {
      output: '',
      error: `Network error: ${String(error)}`
    };
  }
}

// Initialize Python backend - checks connectivity
export async function initializePythonBackend(): Promise<void> {
  // Backend Python execution is always ready - just verify connectivity
  console.log('Using backend Python execution - verifying API connectivity');
  
  try {
    // Optional: Add a health check endpoint call here if needed
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      // Could make a lightweight API call to verify backend is responsive
      console.log('Python backend ready');
    }
  } catch (error) {
    console.warn('Could not verify Python backend connectivity:', error);
  }
}

export function clearCache() {
  // No longer needed - using backend execution
  console.log('Backend execution - no cache to clear');
} 
### assets/js/utils/pythonRunner.ts END ###

### assets/js/contexts/AuthContext.tsx BEGIN ###
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { notifications } from '@mantine/notifications';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface RegisterData {
  username: string;
  password: string;
  password2: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize authentication state on mount
  useEffect(() => {
    console.log('[AuthContext] Initializing authentication state');
    
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedAccessToken && storedRefreshToken) {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      fetchUserProfile(storedAccessToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  // Create authenticated fetch wrapper with automatic token refresh
  const authenticatedFetch = async (url: string, options: RequestInit = {}) => {
    const token = localStorage.getItem('accessToken');
    
    const headers = {
      ...options.headers,
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    };
    
    let response = await fetch(url, { ...options, headers });
    
    // If we get a 401, try to refresh the token
    if (response.status === 401 && localStorage.getItem('refreshToken')) {
      console.log('[AuthContext] Token expired, refreshing...');
      const newToken = await refreshAccessToken();
      
      if (newToken) {
        // Retry the request with the new token
        headers['Authorization'] = `Bearer ${newToken}`;
        response = await fetch(url, { ...options, headers });
      }
    }
    
    return response;
  };

  // Make authenticatedFetch available globally
  useEffect(() => {
    (window as any).authenticatedFetch = authenticatedFetch;
  }, []);

  const fetchUserProfile = async (token: string) => {
    try {
      const response = await fetch('/api/auth/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        console.log('[AuthContext] User profile loaded:', userData.username);
          setUser(userData);
      } else if (response.status === 401) {
        // Token is invalid, try to refresh
        await refreshAccessToken();
      }
    } catch (error) {
      console.error('[AuthContext] Error fetching user profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshAccessToken = async () => {
    const storedRefreshToken = localStorage.getItem('refreshToken');
    if (!storedRefreshToken) {
      console.log('[AuthContext] No refresh token, logging out');
      await logout();
      return null;
    }

    try {
      const response = await fetch('/api/auth/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: storedRefreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('[AuthContext] Token refreshed successfully');
        
        // Update tokens in state and localStorage
        setAccessToken(data.access);
        localStorage.setItem('accessToken', data.access);
        
        if (data.refresh) {
          setRefreshToken(data.refresh);
          localStorage.setItem('refreshToken', data.refresh);
        }
        
        return data.access;
      } else {
        console.log('[AuthContext] Token refresh failed, logging out');
        await logout();
      }
    } catch (error) {
      console.error('[AuthContext] Error refreshing token:', error);
      await logout();
    }
    
    return null;
  };

  const login = async (username: string, password: string) => {
    console.log('[AuthContext] Logging in user:', username);
    
    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('[AuthContext] Login successful');
        
        // Set state
        setUser(data.user);
        setAccessToken(data.access);
        setRefreshToken(data.refresh);
        
        // Save to localStorage
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        
        notifications.show({
          title: 'Login Successful',
          message: `Welcome back, ${data.user.username}!`,
          color: 'green',
        });
      } else {
        throw new Error(data.error || 'Login failed');
      }
    } catch (error: any) {
      console.error('[AuthContext] Login failed:', error);
      notifications.show({
        title: 'Login Failed',
        message: error.message || 'Invalid credentials',
        color: 'red',
      });
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      const response = await fetch('/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        notifications.show({
          title: 'Registration Successful',
          message: 'Please log in with your credentials',
          color: 'green',
        });
        // Auto-login after registration
        await login(userData.username, userData.password);
      } else {
        throw new Error(Object.values(data).flat().join(', '));
      }
    } catch (error: any) {
      notifications.show({
        title: 'Registration Failed',
        message: error.message,
        color: 'red',
      });
      throw error;
    }
  };

  const logout = async () => {
    console.log('[AuthContext] Logging out user');
    
    try {
      if (refreshToken && accessToken) {
        await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            refresh_token: refreshToken,
          }),
        });
      }
    } catch (error) {
      console.error('[AuthContext] Error during logout:', error);
    } finally {
      // Clear state and localStorage
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      
      console.log('[AuthContext] Logout completed');
    }
  };

  const value = {
    user,
    accessToken,
    refreshToken,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 
### assets/js/contexts/AuthContext.tsx END ###

### assets/js/components/index.ts BEGIN ###
export { ThreadsNav } from "./ThreadsNav/ThreadsNav";
export { Chat } from "./Chat/Chat";
export { PracticeScreen } from "./Practice";
### assets/js/components/index.ts END ###

### assets/js/components/Practice/OutputPanel.tsx BEGIN ###
import React, { useEffect } from 'react';
import { Paper, ScrollArea, Text, Code, Stack, Loader, Center } from '@mantine/core';

interface OutputPanelProps {
  output: string;
  error: string | null;
  isLoading: boolean;
}

export function OutputPanel({ output, error, isLoading }: OutputPanelProps) {
  // Add CSS to force scrollbar visibility
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      /* Force Mantine ScrollArea scrollbar to be visible */
      .mantine-ScrollArea-scrollbar {
        opacity: 1 !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
      }
      
      .mantine-ScrollArea-scrollbar[data-orientation="vertical"] {
        width: 14px !important;
        right: 2px !important;
        top: 2px !important;
        bottom: 2px !important;
      }
      
      .mantine-ScrollArea-scrollbar[data-orientation="horizontal"] {
        height: 14px !important;
        left: 2px !important;
        right: 2px !important;
        bottom: 2px !important;
      }
      
      .mantine-ScrollArea-thumb {
        opacity: 1 !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
        cursor: pointer !important;
        transition: background-color 0.2s !important;
      }
      
      .mantine-ScrollArea-thumb:hover {
        background-color: rgba(255, 255, 255, 0.6) !important;
      }
      
      .mantine-ScrollArea-thumb:active {
        background-color: rgba(255, 255, 255, 0.8) !important;
      }
      
      /* Ensure viewport doesn't hide content */
      .mantine-ScrollArea-viewport {
        padding-right: 16px !important;
        padding-bottom: 16px !important;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);
  return (
    <Paper 
      shadow="sm" 
      radius="md" 
      p="sm" 
      style={{ 
        display: 'flex', 
        flexDirection: 'column',
        backgroundColor: 'var(--mantine-color-gray-0)',
        height: '100%',
        width: '100%',
        overflow: 'hidden'
      }}
    >
      <Text size="sm" fw={600} mb="xs" style={{ flexShrink: 0 }}>Output</Text>
      
      <div style={{ 
        flex: 1, 
        backgroundColor: '#1e1e1e',
        borderRadius: '4px',
        display: 'flex',
        flexDirection: 'column',
        minHeight: 0,
        position: 'relative'
      }}>
        <ScrollArea 
          type="always"
          scrollbarSize={14}
          scrollbars="xy"
          style={{ 
            flex: 1,
            padding: '12px'
          }}
        >
        <div style={{ minHeight: '100%', minWidth: 'max-content' }}>
          {isLoading ? (
            <Center h="100%">
              <Loader size="sm" />
            </Center>
          ) : (
            <Stack gap="xs">
              {error ? (
                <Code 
                  block 
                  color="red" 
                  style={{ 
                    backgroundColor: 'transparent', 
                    color: '#ff6b6b',
                    whiteSpace: 'pre',
                    display: 'block',
                    overflowX: 'visible'
                  }}
                >
                  {error}
                </Code>
              ) : output ? (
                <Code 
                  block 
                  style={{ 
                    backgroundColor: 'transparent', 
                    color: '#4caf50',
                    whiteSpace: 'pre',
                    display: 'block',
                    overflowX: 'visible'
                  }}
                >
                  {output}
                </Code>
              ) : (
                <Text size="sm" c="dimmed" style={{ fontFamily: 'monospace' }}>
                  {'> Output will appear here...'}
                </Text>
              )}
            </Stack>
          )}
        </div>
        </ScrollArea>
      </div>
    </Paper>
  );
} 
### assets/js/components/Practice/OutputPanel.tsx END ###

### assets/js/components/Practice/Practice.module.css BEGIN ###
.practiceContainer {
  height: 100vh;
  overflow: hidden;
}

.chatSection {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--mantine-color-gray-0);
  border-right: 1px solid var(--mantine-color-gray-2);
}

.codeSection {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editorWrapper {
  flex: 2;
  min-height: 0;
}

.outputWrapper {
  flex: 1;
  min-height: 0;
} 
### assets/js/components/Practice/Practice.module.css END ###

### assets/js/components/Practice/UserStats.tsx BEGIN ###
import React from 'react';
import { Paper, Group, Text, Stack, Badge, Slider, Box } from '@mantine/core';
import { IconUser, IconTrophy, IconTarget, IconChartBar, IconCheck, IconStar, IconAdjustments } from '@tabler/icons-react';

interface UserStatsProps {
  username: string;
  currentLevel: number;
  manualLevel: number;
  totalQuestions: number;
  correctAnswers: number;
  successRate: number;
  averageGrade: number;
  onLevelChange: (level: number) => void;
  disabled?: boolean;
}

export function UserStats({ 
  username, 
  currentLevel, 
  manualLevel, 
  totalQuestions, 
  correctAnswers, 
  successRate, 
  averageGrade, 
  onLevelChange,
  disabled = false
}: UserStatsProps) {
  return (
    <Paper 
      shadow="sm" 
      radius="md" 
      p="md" 
      withBorder
      style={{ backgroundColor: 'var(--mantine-color-gray-0)', minWidth: '380px' }}
    >
      <Stack gap="md">
        <Group justify="space-between" wrap="nowrap">
          <Group gap="xs">
            <IconUser size={20} style={{ color: 'var(--mantine-color-blue-6)' }} />
            <Text fw={600} size="sm">{username}</Text>
          </Group>
          <Box style={{ minWidth: 160 }}>
            <Group gap="xs" justify="flex-end">
              <IconAdjustments size={16} style={{ color: disabled ? 'var(--mantine-color-gray-4)' : 'var(--mantine-color-gray-6)' }} />
              <Text size="xs" c={disabled ? 'dimmed' : 'dimmed'}>Difficulty Level</Text>
            </Group>
            <Slider
              value={manualLevel}
              onChange={disabled ? () => {} : onLevelChange}
              min={1}
              max={5}
              step={1}
              size="sm"
              color={disabled ? 'gray' : getLevelColor(manualLevel)}
              marks={[
                { value: 1, label: '1' },
                { value: 2, label: '2' },
                { value: 3, label: '3' },
                { value: 4, label: '4' },
                { value: 5, label: '5' },
              ]}
              styles={{
                mark: { fontSize: '15px' },
                markLabel: { fontSize: '15px' },
                thumb: {
                  backgroundColor: disabled ? 'white' : undefined,
                  borderColor: disabled ? 'var(--mantine-color-gray-4)' : undefined,
                  cursor: disabled ? 'not-allowed' : 'pointer',
                  width: '14px',
                  height: '14px',
                  border: disabled ? '2px solid var(--mantine-color-gray-4)' : undefined
                },
                track: disabled ? {
                  backgroundColor: 'var(--mantine-color-gray-3)',
                  cursor: 'not-allowed'
                } : undefined,
                bar: disabled ? {
                  backgroundColor: 'var(--mantine-color-gray-4)',
                } : undefined,
                root: disabled ? {
                  cursor: 'not-allowed'
                } : undefined
              }}
            />
          </Box>
        </Group>
        
        <Stack gap="sm" style={{ paddingTop: '18px', paddingBottom: '4px' }}>
          <Group gap="lg" justify="space-between">
            <Group gap="xs">
              <IconTarget size={18} style={{ color: 'var(--mantine-color-gray-6)' }} />
              <Text size="sm" c="dimmed">Questions: {totalQuestions}</Text>
            </Group>
            <Group gap="xs">
              <IconCheck size={18} style={{ color: 'var(--mantine-color-green-6)' }} />
              <Text size="sm" c="dimmed">Correct: {correctAnswers}</Text>
            </Group>
          </Group>
          <Group gap="lg" justify="space-between">
            <Group gap="xs">
              <IconChartBar size={18} style={{ color: 'var(--mantine-color-gray-6)' }} />
              <Text size="sm" c="dimmed">Success: {successRate}%</Text>
            </Group>
            <Group gap="xs">
              <IconStar size={18} style={{ color: 'var(--mantine-color-yellow-6)' }} />
              <Text size="sm" c="dimmed">Average Grade: {averageGrade.toFixed(1)}/10</Text>
            </Group>
          </Group>
        </Stack>
      </Stack>
    </Paper>
  );
}

function getLevelColor(level: number): string {
  switch (level) {
    case 1:
      return 'green';
    case 2:
      return 'lime';
    case 3:
      return 'yellow';
    case 4:
      return 'orange';
    case 5:
      return 'red';
    default:
      return 'gray';
  }
} 
### assets/js/components/Practice/UserStats.tsx END ###

### assets/js/components/Practice/PracticeScreen.tsx BEGIN ###
import React, { useState, useEffect, useRef } from 'react';
import { ScrollArea, Stack, Group, Button, Box } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconLogout } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { UserStats } from './UserStats';
import { LevelSuggestionModal } from './LevelSuggestionModal';
import { QuestionDisplay } from './QuestionDisplay';
import { PythonEditor } from './PythonEditor';
import { OutputPanel } from './OutputPanel';
import { initializePythonBackend, runPythonCode } from '../../utils/pythonRunner';

interface UserStatsData {
  username: string;
  current_level: number;
  manual_level: number;
  total_questions_attempted: number;
  correct_answers_count: number;
  success_rate: number;
  average_grade: number;
}

interface Question {
  id: number;
  instruction: string;
  input: string;
  output: string;
  difficulty_level: number;
}

interface Message {
  id: string;
  type: 'system' | 'question' | 'feedback';
  content: string;
  grade?: number;
  timestamp: Date;
}

interface LevelSuggestion {
  type: 'level_up' | 'level_down';
  current_level: number;
  suggested_level: number;
  reason: string;
}

export function PracticeScreen() {
  // Ensure no body margin/padding
  React.useEffect(() => {
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.height = '100vh';
    document.body.style.overflow = 'hidden';
  }, []);

  const { user, accessToken, logout } = useAuth();
  const [userStats, setUserStats] = useState<UserStatsData>({
    username: '',
    current_level: 3,
    manual_level: 3,
    total_questions_attempted: 0,
    correct_answers_count: 0,
    success_rate: 0,
    average_grade: 0.0
  });
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isAbandoning, setIsAbandoning] = useState(false);
  const [showNextButton, setShowNextButton] = useState(false);
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);
  const [levelSuggestion, setLevelSuggestion] = useState<LevelSuggestion | null>(null);
  const [showLevelModal, setShowLevelModal] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const levelChangeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Store user ID in a ref to avoid re-creating saveProgress
  const userIdRef = useRef<number | undefined>(user?.id);
  useEffect(() => {
    userIdRef.current = user?.id;
  }, [user?.id]);

  // Auto-save code to localStorage
  const saveProgress = React.useCallback(() => {
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setTimeout(() => {
      if (currentQuestion && code) {
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.setItem(progressKey, JSON.stringify({
          code,
          questionId: currentQuestion.id,
          timestamp: Date.now()
        }));
        console.log('[PracticeScreen] Code auto-saved');
      }
    }, 1000); // Save after 1 second of no changes
  }, [code, currentQuestion]);

  // Save code whenever it changes
  useEffect(() => {
    saveProgress();
  }, [code, saveProgress]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
      if (levelChangeTimeoutRef.current) {
        clearTimeout(levelChangeTimeoutRef.current);
      }
    };
  }, []);

  // Load Python backend and fetch initial data on mount
  const isInitializedRef = useRef(false);
  
  useEffect(() => {
    if (!accessToken || isInitializedRef.current) return;

    // Mark as initialized to prevent re-running
    isInitializedRef.current = true;

    // Initialize Python backend
    initializePythonBackend().then(() => {
      console.log('Python backend initialized for practice screen');
    }).catch((error) => {
      console.error('Failed to initialize Python backend:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to initialize Python runtime',
        color: 'red'
      });
    });

    // Add welcome message
    const displayName = user?.first_name || user?.username || 'there';
    setMessages([{
      id: '1',
      type: 'system',
      content: `Welcome ${displayName}! Let's start practicing Python coding problems.`,
      timestamp: new Date()
    }]);

    fetchUserStats();
    fetchNextQuestion();
  }, [!!accessToken]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      // Check if the last message is a feedback message
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.type === 'feedback') {
        // Set up callback for when feedback element is mounted
        (window as any).__feedbackCallback = {
          onFeedbackMount: (element: HTMLDivElement) => {
            // Small delay to ensure element is fully rendered
            setTimeout(() => {
              element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest' 
              });
            }, 100);
          }
        };
      } else {
        // For other messages, scroll to bottom
        scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
      }
    }
  }, [messages]);

  const fetchUserStats = async () => {
    try {
      const response = await (window as any).authenticatedFetch('/api/practice/user-stats/');

      if (response.ok) {
        const data = await response.json();
        setUserStats(data);
      }
    } catch (error) {
      console.error('Error fetching user stats:', error);
    }
  };

  const setManualLevel = async (level: number) => {
    // Clear any existing timeout
    if (levelChangeTimeoutRef.current) {
      clearTimeout(levelChangeTimeoutRef.current);
    }

    // Update the level in the UI immediately for responsiveness
    setUserStats(prev => ({ ...prev, manual_level: level }));

         // Debounce the API call
     levelChangeTimeoutRef.current = setTimeout(async () => {
       try {
         const response = await (window as any).authenticatedFetch('/api/practice/set-manual-level/', {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json'
           },
           body: JSON.stringify({ level })
         });

        if (response.ok) {
          const data = await response.json();
          setUserStats(data.user_stats);
          notifications.show({
            title: 'Level Updated',
            message: `Difficulty level set to ${level}`,
            color: 'blue'
          });
        }
      } catch (error) {
        console.error('Error setting manual level:', error);
        notifications.show({
          title: 'Error',
          message: 'Failed to update difficulty level',
          color: 'red'
        });
        // Revert the UI change if API call failed
        await fetchUserStats();
      }
    }, 1000); // Wait 1 second after user stops changing level
  };

  const fetchNextQuestion = async () => {
    try {
      const response = await (window as any).authenticatedFetch('/api/practice/next-question/');

      if (response.ok) {
        const data = await response.json();
        setCurrentQuestion(data.question);
        setUserStats(data.user_stats);
        
        // Add the current question to messages
        const questionMessage: Message = {
          id: Date.now().toString(),
          type: 'question',
          content: formatQuestionContent(data.question),
          timestamp: new Date()
        };
        
        // Clear any previous questions/feedback and keep only welcome message + current question
        setMessages(prev => {
          const welcomeMessage = prev.find(msg => msg.type === 'system');
          return welcomeMessage ? [welcomeMessage, questionMessage] : [questionMessage];
        });
        
        // Check for saved code for this question
        const progressKey = `practice_code_${userIdRef.current}_${data.question.id}`;
        const savedProgress = localStorage.getItem(progressKey);
        
        if (savedProgress) {
          try {
            const { code: savedCode } = JSON.parse(savedProgress);
            setCode(savedCode);
            console.log('[PracticeScreen] Restored saved code for question');
          } catch (error) {
            console.error('[PracticeScreen] Error restoring saved code:', error);
            setCode('');
          }
        } else {
          setCode('');
        }

        setOutput('');
        setError(null);
        setShowNextButton(false); // Hide next button for new question
        setIsSubmitDisabled(false); // Re-enable submit button for new question
      }
    } catch (error) {
      console.error('Error fetching next question:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to fetch next question',
        color: 'red'
      });
    }
  };

  const formatQuestionContent = (question: Question): string => {
    let content = `**Problem:**\n${question.instruction}\n\n`;
    if (question.input) {
      content += `**Input:**\n${question.input}`;
    }
    return content;
  };

  const runCode = async () => {
    setIsRunning(true);
    setError(null);
    setOutput('');

    try {
      console.log('Running code:', code.substring(0, 50) + '...');
      console.log('Auth token available:', !!accessToken);
      const result = await runPythonCode(code);
      console.log('Code execution result:', result);
      
      if (result.error) {
        console.error('Python execution error:', result.error);
        setError(result.error);
      } else if (result.output) {
        setOutput(result.output);
      } else {
        setOutput('(No output)');
      }
    } catch (error) {
      console.error('Error running Python code:', error);
      setError(`JavaScript Error: ${String(error)}`);
    } finally {
      setIsRunning(false);
    }
  };

  const submitCode = async () => {
    if (!currentQuestion) return;

    setIsSubmitting(true);
    
    // First, clear output and error states (like runCode does)
    setError(null);
    setOutput('');
    
    try {
      // First run the code to get output
      console.log('Submitting code:', code.substring(0, 50) + '...');
      console.log('Auth token available:', !!accessToken);
      
      let result;
      try {
        result = await runPythonCode(code);
        console.log('Code execution result:', result);
      } catch (error) {
        console.error('Error running Python code:', error);
        setError(`JavaScript Error: ${String(error)}`);
        setIsSubmitting(false);
        return;
      }
      
      // Display the output in the output panel (like runCode does)
      if (result.error) {
        console.error('Python execution error:', result.error);
        setError(result.error);
      } else if (result.output) {
        setOutput(result.output);
      } else {
        setOutput('(No output)');
      }
      
      // Store the output for backend submission
      const codeOutput = result.output || '';
      const codeError = result.error || null;
      
      // Submit to backend
      const response = await (window as any).authenticatedFetch('/api/practice/submit-solution/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          code: code
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        // Add feedback message with expected output
        const feedbackContent = {
          expectedOutput: currentQuestion.output,
          feedback: result.feedback,
          grade: result.grade
        };
        
        const feedbackMessage: Message = {
          id: Date.now().toString(),
          type: 'feedback',
          content: JSON.stringify(feedbackContent),
          grade: result.grade,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, feedbackMessage]);

        // Update user stats
        await fetchUserStats();

        // Handle level suggestion
        if (result.level_suggestion) {
          setLevelSuggestion(result.level_suggestion);
          setShowLevelModal(true);
        }

        // Show next button and disable submit button
        setShowNextButton(true);
        setIsSubmitDisabled(true);
        
        // Clear saved progress for this question since it's been submitted
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.removeItem(progressKey);
        console.log('[PracticeScreen] Cleared saved code after successful submission');
      }
    } catch (error) {
      console.error('Error submitting code:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to submit solution',
        color: 'red'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLevelSuggestionAccept = async () => {
    if (!levelSuggestion) return;
    
    await setManualLevel(levelSuggestion.suggested_level);
    
    // Show level change notification after user accepts
    notifications.show({
      title: 'Level Changed!',
      message: `You are now at Level ${levelSuggestion.suggested_level}`,
      color: 'blue'
    });
    
    setShowLevelModal(false);
    setLevelSuggestion(null);
  };

  const handleLevelSuggestionDecline = () => {
    setShowLevelModal(false);
    setLevelSuggestion(null);
  };

  const handleLogout = async () => {
    try {
      await logout();
      notifications.show({
        title: 'Logged Out',
        message: 'You have been successfully logged out',
        color: 'green'
      });
    } catch (error) {
      console.error('Logout error:', error);
      notifications.show({
        title: 'Logout Error',
        message: 'There was an issue logging out',
        color: 'red'
      });
    }
  };

  const handleNextProblem = async () => {
    setShowNextButton(false);
    await fetchNextQuestion();
  };

  const abandonQuestion = async () => {
    if (!currentQuestion) return;

    setIsAbandoning(true);
    
         try {
       const response = await (window as any).authenticatedFetch('/api/practice/abandon-question/', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json'
         }
       });

      if (response.ok) {
        const result = await response.json();
        
        // Show the expected output as solution (without grade or feedback)
        const solutionContent = {
          expectedOutput: currentQuestion.output,
          feedback: null,
          grade: null,
          isSkipped: true
        };
        
        const solutionMessage: Message = {
          id: Date.now().toString(),
          type: 'feedback',
          content: JSON.stringify(solutionContent),
          timestamp: new Date()
        };
        setMessages(prev => [...prev, solutionMessage]);
        
        // Update user stats
        await fetchUserStats();

        // Handle level suggestion
        if (result.level_suggestion) {
          setLevelSuggestion(result.level_suggestion);
          setShowLevelModal(true);
        }

        // Show abandonment notification
        notifications.show({
          title: 'Question Skipped',
          message: 'The question has been skipped, recorded as a failed attempt and graded as 0',
          color: 'orange'
        });

        // Clear saved progress for this question
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.removeItem(progressKey);
        
        // Show next button and disable submit button
        setShowNextButton(true);
        setIsSubmitDisabled(true);
      }
    } catch (error) {
      console.error('Error abandoning question:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to abandon question',
        color: 'red'
      });
    } finally {
      setIsAbandoning(false);
    }
  };

  return (
    <div style={{ 
      height: '100vh', 
      width: '100vw', 
      overflow: 'hidden', 
      display: 'flex', 
      padding: '16px', 
      gap: '16px',
      boxSizing: 'border-box'
    }}>
      {/* Left side - Chat UI */}
      <div style={{ 
        flex: '0 0 40%', 
        height: '100%', 
        overflow: 'hidden', 
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        <Stack gap="md" style={{ height: '100%', flex: 1 }}>
            <Group justify="space-between" align="flex-start">
              <UserStats 
                username={userStats.username}
                currentLevel={userStats.current_level}
                manualLevel={userStats.manual_level}
                totalQuestions={userStats.total_questions_attempted}
                correctAnswers={userStats.correct_answers_count}
                successRate={userStats.success_rate}
                averageGrade={userStats.average_grade}
                onLevelChange={setManualLevel}
                disabled={!showNextButton}
              />
              <Button 
                variant="light" 
                color="red" 
                leftSection={<IconLogout size={16} />}
                style={{
                  marginTop: 12,
                  border: 'none',
                  '&:hover': {
                    backgroundColor: 'var(--mantine-color-red-7)',
                  }
                }}
                onClick={handleLogout}
              >
                Logout
              </Button>
            </Group>
            
            <Box style={{ 
              flex: 1, 
              position: 'relative', 
              minHeight: 0,
              maxHeight: '100%',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <ScrollArea 
                style={{ 
                  height: '80vh',
                  width: '100%',
                  minHeight: 0
                }} 
                viewportRef={scrollAreaRef}
                type="auto"
                scrollbarSize={12}
                scrollbars="y"
                styles={(theme) => ({
                  viewport: {
                    paddingBottom: '16px',
                  },
                  scrollbar: {
                    width: 14,
                    paddingLeft: 2,
                    paddingRight: 2,
                    zIndex: 10,
                  },
                  thumb: {
                    backgroundColor: theme.colors.gray[5],
                  },
                  root: {
                    height: '100%'
                  },
                })}
              >
                <QuestionDisplay messages={messages} />
              </ScrollArea>
            </Box>
        </Stack>
      </div>

      {/* Right side - Code Editor and Output */}
      <div style={{ flex: '1', height: '100%', overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        <div style={{ flex: '1.5', minHeight: 0, display: 'flex', overflow: 'hidden' }}>
          <PythonEditor
            code={code}
            onChange={setCode}
            onRun={runCode}
            onSubmit={submitCode}
            onAbandon={abandonQuestion}
            isRunning={isRunning}
            isSubmitting={isSubmitting}
            isAbandoning={isAbandoning}
            isSubmitDisabled={isSubmitDisabled}
            showNextButton={showNextButton}
            onNextProblem={handleNextProblem}
          />
        </div>
        
        <div style={{ flex: '1', minHeight: 0, display: 'flex', overflow: 'hidden' }}>
          <OutputPanel
            output={output}
            error={error}
            isLoading={isRunning}
          />
        </div>
      </div>

      {/* Level Suggestion Modal */}
      <LevelSuggestionModal
        isOpen={showLevelModal}
        suggestion={levelSuggestion}
        onAccept={handleLevelSuggestionAccept}
        onDecline={handleLevelSuggestionDecline}
        onClose={handleLevelSuggestionDecline}
      />
    </div>
  );
} 
### assets/js/components/Practice/PracticeScreen.tsx END ###

### assets/js/components/Practice/PythonEditor.tsx BEGIN ###
import React, { useRef, useEffect, useState } from 'react';
import AceEditor from 'react-ace';
import { Button, Group, Paper } from '@mantine/core';
import { IconPlayerPlay, IconSend } from '@tabler/icons-react';

import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/ext-language_tools';

interface PythonEditorProps {
  code: string;
  onChange: (code: string) => void;
  onRun: () => void;
  onSubmit: () => void;
  onAbandon?: () => void;
  isRunning: boolean;
  isSubmitting: boolean;
  isAbandoning?: boolean;
  isSubmitDisabled?: boolean;
  showNextButton?: boolean;
  onNextProblem?: () => void;
}

export function PythonEditor({ 
  code, 
  onChange, 
  onRun, 
  onSubmit, 
  onAbandon,
  isRunning, 
  isSubmitting,
  isAbandoning = false,
  isSubmitDisabled = false,
  showNextButton = false,
  onNextProblem
}: PythonEditorProps) {
  const editorRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [editorHeight, setEditorHeight] = useState('400px');

  useEffect(() => {
    // Calculate available height
    const updateHeight = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const buttonHeight = 60; // Approximate height of buttons + margins
        const availableHeight = rect.height - buttonHeight;
        setEditorHeight(`${Math.max(300, availableHeight)}px`);
      }
    };

    updateHeight();
    window.addEventListener('resize', updateHeight);
    
    // Force update after a short delay to ensure layout is complete
    setTimeout(updateHeight, 100);
    
    // Force editor refresh to show scrollbars
    setTimeout(() => {
      if (editorRef.current && editorRef.current.editor) {
        editorRef.current.editor.resize();
        editorRef.current.editor.renderer.updateFull();
      }
    }, 200);

    return () => {
      window.removeEventListener('resize', updateHeight);
    };
  }, []);

  // Add CSS for visible scrollbars
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      /* Make scrollbar track visible */
      .ace_scrollbar {
        opacity: 1 !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
      }
      
      /* Vertical scrollbar */
      .ace_scrollbar-v {
        width: 14px !important;
        right: 0 !important;
        cursor: pointer !important;
      }
      
      /* Horizontal scrollbar */
      .ace_scrollbar-h {
        height: 14px !important;
        bottom: 0 !important;
        cursor: pointer !important;
      }
      
      /* Scrollbar thumb (the draggable part) */
      .ace_scrollbar-inner {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
      }
      
      /* Scrollbar thumb on hover */
      .ace_scrollbar-inner:hover {
        background-color: rgba(255, 255, 255, 0.6) !important;
      }
      
      /* Scrollbar thumb when active/dragging */
      .ace_scrollbar-inner:active {
        background-color: rgba(255, 255, 255, 0.8) !important;
      }
      
      /* Ensure the corner between scrollbars is visible */
      .ace_scroller {
        margin-right: 0 !important;
      }
      
      /* Fallback: Native scrollbar styling for webkit browsers */
      .ace_content::-webkit-scrollbar,
      .ace_scroller::-webkit-scrollbar {
        width: 14px !important;
        height: 14px !important;
      }
      
      .ace_content::-webkit-scrollbar-track,
      .ace_scroller::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3) !important;
      }
      
      .ace_content::-webkit-scrollbar-thumb,
      .ace_scroller::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
      }
      
      .ace_content::-webkit-scrollbar-thumb:hover,
      .ace_scroller::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.6) !important;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <Paper 
      ref={containerRef}
      shadow="sm" 
      radius="md" 
      p="sm" 
      style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%' }}
    >
      <Group justify="flex-start" gap="sm" mb="sm">
        <Button
          leftSection={<IconPlayerPlay size={16} />}
          variant="light"
          onClick={onRun}
          loading={isRunning}
          disabled={isSubmitting}
        >
          Run
        </Button>
        <Button
          leftSection={<IconSend size={16} />}
          onClick={onSubmit}
          loading={isSubmitting}
          disabled={isRunning || isSubmitDisabled}
        >
          Submit
        </Button>
        {onAbandon && (
          <Button
            variant="light"
            color="orange"
            onClick={onAbandon}
            loading={isAbandoning}
            disabled={isRunning || isSubmitting || showNextButton}
          >
            Skip Question
          </Button>
        )}
        {showNextButton && onNextProblem && (
          <Button
            variant="filled"
            color="blue"
            onClick={onNextProblem}
            disabled={isRunning || isSubmitting}
          >
            Next Problem
          </Button>
        )}
      </Group>
      
      <div style={{ flex: 1, border: '1px solid var(--mantine-color-gray-3)', borderRadius: '4px', overflow: 'visible', position: 'relative' }}>
        <AceEditor
          ref={editorRef}
          mode="python"
          theme="monokai"
          onChange={onChange}
          value={code}
          name="python-editor"
          wrapEnabled={false}
          editorProps={{ $blockScrolling: true }}
          onLoad={(editor) => {
            // Force scrollbar visibility
            editor.setShowInvisibles(false);
            editor.renderer.setScrollMargin(0, 0, 0, 0);
            editor.renderer.setPadding(10);
            
            // Update scrollbar settings
            editor.setOptions({
              animatedScroll: false
            });
            
            // Force a resize to show scrollbars
            setTimeout(() => {
              editor.resize();
              editor.renderer.updateFull();
            }, 100);
          }}
          setOptions={{
            enableBasicAutocompletion: false,
            enableLiveAutocompletion: false,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 4,
            useWorker: false,
            showInvisibles: false,
            displayIndentGuides: true,
            scrollPastEnd: true,
            animatedScroll: false
          }}
          fontSize={14}
          width="100%"
          height={editorHeight}
          style={{
            lineHeight: '1.5'
          }}
        />
      </div>
    </Paper>
  );
} 
### assets/js/components/Practice/PythonEditor.tsx END ###

### assets/js/components/Practice/LevelSuggestionModal.tsx BEGIN ###
import React from 'react';
import { Modal, Text, Group, Button, Stack, Alert } from '@mantine/core';
import { IconTrendingUp, IconTrendingDown, IconInfoCircle } from '@tabler/icons-react';

interface LevelSuggestion {
  type: 'level_up' | 'level_down';
  current_level: number;
  suggested_level: number;
  reason: string;
}

interface LevelSuggestionModalProps {
  isOpen: boolean;
  suggestion: LevelSuggestion | null;
  onAccept: () => void;
  onDecline: () => void;
  onClose: () => void;
}

export function LevelSuggestionModal({ 
  isOpen, 
  suggestion, 
  onAccept, 
  onDecline, 
  onClose 
}: LevelSuggestionModalProps) {
  if (!suggestion) return null;

  const isLevelUp = suggestion.type === 'level_up';
  const icon = isLevelUp ? <IconTrendingUp size={24} /> : <IconTrendingDown size={24} />;
  const color = isLevelUp ? 'green' : 'orange';
  const title = isLevelUp ? 'Level Up Suggestion' : 'Level Down Suggestion';

  return (
    <Modal
      opened={isOpen}
      onClose={onClose}
      title={title}
      size="sm"
      centered
      withCloseButton={false}
      closeOnClickOutside={false}
      closeOnEscape={false}
    >
      <Stack gap="md">
        <Alert
          icon={icon}
          color={color}
          variant="light"
        >
          <Text size="sm">
            {suggestion.reason}
          </Text>
        </Alert>

        <Stack gap="xs">
          <Text size="sm" fw={500}>
            Would you like to change your difficulty level?
          </Text>
          <Group gap="xs">
            <Text size="sm" c="dimmed">
              Current Level: {suggestion.current_level}
            </Text>
            <Text size="sm" c="dimmed">
              →
            </Text>
            <Text size="sm" c="dimmed">
              Suggested Level: {suggestion.suggested_level}
            </Text>
          </Group>
        </Stack>

        <Group justify="flex-end" gap="sm">
          <Button
            variant="light"
            color="gray"
            onClick={onDecline}
            size="sm"
          >
            Keep Current Level
          </Button>
          <Button
            color={color}
            onClick={onAccept}
            size="sm"
          >
            {isLevelUp ? 'Level Up' : 'Level Down'}
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
} 
### assets/js/components/Practice/LevelSuggestionModal.tsx END ###

### assets/js/components/Practice/QuestionDisplay.tsx BEGIN ###
import React from 'react';
import { Paper, Text, Stack, Badge, Group, Avatar, Card, List, ThemeIcon } from '@mantine/core';
import { IconRobot, IconUser, IconCheck, IconX } from '@tabler/icons-react';
import Markdown from 'react-markdown';

interface Message {
  id: string;
  type: 'system' | 'question' | 'feedback';
  content: string;
  grade?: number;
  timestamp: Date;
}

interface QuestionDisplayProps {
  messages: Message[];
  onFeedbackMount?: (element: HTMLDivElement) => void;
}

export function QuestionDisplay({ messages, onFeedbackMount }: QuestionDisplayProps) {
  return (
    <Stack 
      gap="md" 
      style={{ 
        padding: '16px',
        paddingBottom: '16px',
        minHeight: 'fit-content',
        width: '100%',
        boxSizing: 'border-box'
      }}
    >
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
    </Stack>
  );
}

function MessageItem({ message }: { message: Message }) {
  const feedbackRef = React.useRef<HTMLDivElement>(null);
  
  React.useEffect(() => {
    if (message.type === 'feedback' && feedbackRef.current) {
      const { onFeedbackMount } = (window as any).__feedbackCallback || {};
      if (onFeedbackMount) {
        onFeedbackMount(feedbackRef.current);
      }
    }
  }, [message.type]);

  if (message.type === 'system') {
    return (
      <Group gap="sm" align="flex-start">
        <Avatar color="blue" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Paper 
          shadow="xs" 
          p="md" 
          radius="md" 
          style={{ 
            flex: 1,
            backgroundColor: 'var(--mantine-color-blue-0)'
          }}
        >
          <Text size="sm">{message.content}</Text>
        </Paper>
      </Group>
    );
  }

  if (message.type === 'question') {
    return (
      <Group gap="sm" align="flex-start">
        <Avatar color="teal" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ flex: 1 }}>
          <Stack gap="sm">
            <Group justify="space-between">
              <Text fw={600}>New Question</Text>
              <Badge variant="light" color="teal">
                Practice Problem
              </Badge>
            </Group>
            <Markdown>{message.content}</Markdown>
          </Stack>
        </Card>
      </Group>
    );
  }

  if (message.type === 'feedback') {
    const gradeColor = getGradeColor(message.grade || 0);
    
    return (
      <Group gap="sm" align="flex-start" ref={feedbackRef}>
        <Avatar color="grape" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ flex: 1 }}>
          <Stack gap="md">
            <Group justify="space-between">
              <Text fw={600}>Feedback</Text>
              {message.grade !== undefined && (
                <Badge 
                  size="lg" 
                  color={gradeColor}
                  variant="filled"
                >
                  Grade: {message.grade}/10
                </Badge>
              )}
            </Group>
            
            <FeedbackContent content={message.content} />
          </Stack>
        </Card>
      </Group>
    );
  }

  return null;
}

function FeedbackContent({ content }: { content: string }) {
  try {
    const data = JSON.parse(content);
    
    // Handle skipped questions (expectedOutput but no feedback)
    if (data.expectedOutput && data.feedback === null) {
      return (
        <Stack gap="sm">
          <div>
            <Text size="sm" fw={500} mb={4} c="blue">Solution:</Text>
            <Paper 
              p="xs" 
              radius="sm" 
              style={{ 
                backgroundColor: 'var(--mantine-color-blue-0)',
                overflowX: 'auto',
                maxWidth: '100%'
              }}
            >
              <Text 
                size="sm" 
                style={{ 
                  fontFamily: 'monospace', 
                  whiteSpace: 'pre',
                  display: 'block'
                }}
              >
                {data.expectedOutput}
              </Text>
            </Paper>
          </div>
        </Stack>
      );
    }
    
    // Handle new format with expectedOutput and feedback
    if (data.expectedOutput && data.feedback) {
      const feedback = data.feedback;
      return (
        <Stack gap="sm">
          {/* Show Expected Output first */}
          <div>
            <Text size="sm" fw={500} mb={4} c="blue">Solution:</Text>
            <Paper 
              p="xs" 
              radius="sm" 
              style={{ 
                backgroundColor: 'var(--mantine-color-blue-0)',
                overflowX: 'auto',
                maxWidth: '100%'
              }}
            >
              <Text 
                size="sm" 
                style={{ 
                  fontFamily: 'monospace', 
                  whiteSpace: 'pre',
                  display: 'block'
                }}
              >
                {data.expectedOutput}
              </Text>
            </Paper>
          </div>
          
          {/* Then show feedback */}
          <Text size="sm" fw={600}>{feedback.overall}</Text>
          
          <List size="sm" spacing="xs" mt={8}>
            {feedback.correctness && feedback.correctness.message && feedback.correctness.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Correctness (40%):</Text> {feedback.correctness.score !== undefined ? `${(feedback.correctness.score * 10).toFixed(1)} - ` : ''}{feedback.correctness.message}
                  </Text>
                  {(feedback.correctness.issues?.length > 0 || feedback.correctness.strengths?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.correctness.issues?.map((issue: string, idx: number) => (
                        <List.Item key={`issue-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                      {feedback.correctness.strengths?.map((strength: string, idx: number) => (
                        <List.Item key={`strength-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{strength}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.code_quality && feedback.code_quality.message && feedback.code_quality.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Code Quality (30%):</Text> {feedback.code_quality.score !== undefined ? `${(feedback.code_quality.score * 10).toFixed(1)} - ` : ''}{feedback.code_quality.message}
                  </Text>
                  {feedback.code_quality.issues?.length > 0 && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.code_quality.issues.map((issue: string, idx: number) => (
                        <List.Item key={idx} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.efficiency && feedback.efficiency.message && feedback.efficiency.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Efficiency (20%):</Text> {feedback.efficiency.score !== undefined ? `${(feedback.efficiency.score * 10).toFixed(1)} - ` : ''}{feedback.efficiency.message}
                  </Text>
                  {(feedback.efficiency.inefficiencies?.length > 0 || feedback.efficiency.suggestions?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.efficiency.inefficiencies?.map((issue: string, idx: number) => (
                        <List.Item key={`ineff-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                      {feedback.efficiency.suggestions?.map((suggestion: string, idx: number) => (
                        <List.Item key={`sugg-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{suggestion}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.sophistication && feedback.sophistication.message && feedback.sophistication.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Sophistication (10%):</Text> {feedback.sophistication.score !== undefined ? `${(feedback.sophistication.score * 10).toFixed(1)} - ` : ''}{feedback.sophistication.message}
                  </Text>
                  {(feedback.sophistication.advanced_techniques?.length > 0 || feedback.sophistication.areas_for_improvement?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.sophistication.advanced_techniques?.map((technique: string, idx: number) => (
                        <List.Item key={`tech-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{technique}</Text>
                        </List.Item>
                      ))}
                      {feedback.sophistication.areas_for_improvement?.map((area: string, idx: number) => (
                        <List.Item key={`area-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{area}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
          </List>
        </Stack>
      );
    }
    
    // Handle old format (just feedback)
    const feedback = data.overall ? data : data.feedback || data;
    
    return (
      <Stack gap="sm">
        <Text size="sm" fw={600}>{feedback.overall}</Text>
        
        <List size="sm" spacing="xs" mt={8}>
          {feedback.correctness && feedback.correctness.message && feedback.correctness.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Correctness (40%):</Text> {feedback.correctness.score !== undefined ? `${(feedback.correctness.score * 10).toFixed(1)} - ` : ''}{feedback.correctness.message}
                </Text>
                {(feedback.correctness.issues?.length > 0 || feedback.correctness.strengths?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.correctness.issues?.map((issue: string, idx: number) => (
                      <List.Item key={`issue-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                    {feedback.correctness.strengths?.map((strength: string, idx: number) => (
                      <List.Item key={`strength-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{strength}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.code_quality && feedback.code_quality.message && feedback.code_quality.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Code Quality (30%):</Text> {feedback.code_quality.score !== undefined ? `${(feedback.code_quality.score * 10).toFixed(1)} - ` : ''}{feedback.code_quality.message}
                </Text>
                {feedback.code_quality.issues?.length > 0 && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.code_quality.issues.map((issue: string, idx: number) => (
                      <List.Item key={idx} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.efficiency && feedback.efficiency.message && feedback.efficiency.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Efficiency (20%):</Text> {feedback.efficiency.score !== undefined ? `${(feedback.efficiency.score * 10).toFixed(1)} - ` : ''}{feedback.efficiency.message}
                </Text>
                {(feedback.efficiency.inefficiencies?.length > 0 || feedback.efficiency.suggestions?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.efficiency.inefficiencies?.map((issue: string, idx: number) => (
                      <List.Item key={`ineff-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                    {feedback.efficiency.suggestions?.map((suggestion: string, idx: number) => (
                      <List.Item key={`sugg-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{suggestion}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.sophistication && feedback.sophistication.message && feedback.sophistication.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Sophistication (10%):</Text> {feedback.sophistication.score !== undefined ? `${(feedback.sophistication.score * 10).toFixed(1)} - ` : ''}{feedback.sophistication.message}
                </Text>
                {(feedback.sophistication.advanced_techniques?.length > 0 || feedback.sophistication.areas_for_improvement?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.sophistication.advanced_techniques?.map((technique: string, idx: number) => (
                      <List.Item key={`tech-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{technique}</Text>
                      </List.Item>
                    ))}
                    {feedback.sophistication.areas_for_improvement?.map((area: string, idx: number) => (
                      <List.Item key={`area-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{area}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
        </List>
      </Stack>
    );
  } catch {
    return <Text size="sm">{content}</Text>;
  }
}

function getGradeColor(grade: number): string {
  if (grade >= 9) return 'green';
  if (grade >= 7) return 'lime';
  if (grade >= 5) return 'yellow';
  if (grade >= 3) return 'orange';
  return 'red';
} 
### assets/js/components/Practice/QuestionDisplay.tsx END ###

### assets/js/components/Practice/index.ts BEGIN ###
export { PracticeScreen } from './PracticeScreen';
export { UserStats } from './UserStats';
export { QuestionDisplay } from './QuestionDisplay';
export { PythonEditor } from './PythonEditor';
export { OutputPanel } from './OutputPanel';
export { LevelSuggestionModal } from './LevelSuggestionModal'; 
### assets/js/components/Practice/index.ts END ###

### assets/js/components/Auth/ForgotPassword.tsx BEGIN ###
import React from 'react';
import {
  Container,
  Paper,
  Title,
  Text,
  Button,
  Center,
  Box,
  ThemeIcon,
  Stack,
  Anchor,
} from '@mantine/core';
import { IconMail, IconArrowLeft } from '@tabler/icons-react';
import { Link } from 'react-router-dom';

export function ForgotPassword() {
  // For now, we'll use hardcoded email. This would be fetched from the backend
  const adminEmail = 'roni.shternberg@gmail.com';

  return (
    <Container size={420} my={40}>
      <Button
        component={Link}
        to="/login"
        variant="subtle"
        leftSection={<IconArrowLeft size={16} />}
        mb="xl"
      >
        Back to login
      </Button>

      <Paper withBorder shadow="lg" p={40} radius="md">
        <Center mb="xl">
          <ThemeIcon
            size={64}
            radius="xl"
            variant="light"
            color="blue"
          >
            <IconMail size={32} />
          </ThemeIcon>
        </Center>

        <Title
          order={2}
          ta="center"
          style={{
            fontFamily: `Greycliff CF, sans-serif`,
            fontWeight: 700,
          }}
          mb="md"
        >
          Password Reset
        </Title>

        <Stack spacing="md">
          <Text ta="center" c="dimmed" size="lg">
            Forgot password is not implemented yet.
          </Text>
          
          <Text ta="center" size="md">
            Please contact the site admin at{' '}
            <Anchor href={`mailto:${adminEmail}`} fw={500}>
              {adminEmail}
            </Anchor>
          </Text>
        </Stack>

        <Box mt="xl">
          <Text ta="center" size="sm" c="dimmed">
            We apologize for the inconvenience.
          </Text>
        </Box>
      </Paper>
    </Container>
  );
} 
### assets/js/components/Auth/ForgotPassword.tsx END ###

### assets/js/components/Auth/Register.tsx BEGIN ###
import React, { useState } from 'react';
import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Text,
  Container,
  Group,
  Anchor,
  LoadingOverlay,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconUser, IconLock, IconMail } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export function Register() {
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      username: '',
      email: '',
      password: '',
      password2: '',
      first_name: '',
      last_name: '',
    },
    validate: {
      username: (value: string) => {
        if (!value) return 'Username is required';
        if (value.length < 3) return 'Username must be at least 3 characters';
        return null;
      },
      email: (value: string) => {
        if (!value) return 'Email is required';
        if (!/^\S+@\S+$/.test(value)) return 'Invalid email';
        return null;
      },
      password: (value: string) => {
        if (!value) return 'Password is required';
        if (value.length < 8) return 'Password must be at least 8 characters';
        return null;
      },
      password2: (value: string, values: any) => {
        if (!value) return 'Please confirm your password';
        if (value !== values.password) return 'Passwords do not match';
        return null;
      },
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    try {
      await register(values);
      navigate('/');
    } catch (error) {
      // Error is handled in AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title
        ta="center"
        style={{
          fontFamily: `Greycliff CF, sans-serif`,
          fontWeight: 900,
        }}
      >
        Create an account
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Already have an account?{' '}
        <Anchor component={Link} to="/login" size="sm">
          Sign in
        </Anchor>
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />
        
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Group grow>
            <TextInput
              label="First name"
              placeholder="Your first name"
              {...form.getInputProps('first_name')}
            />
            
            <TextInput
              label="Last name"
              placeholder="Your last name"
              {...form.getInputProps('last_name')}
            />
          </Group>

          <TextInput
            label="Username"
            placeholder="Choose a username"
            leftSection={<IconUser size={16} />}
            required
            mt="md"
            {...form.getInputProps('username')}
          />
          
          <TextInput
            label="Email"
            placeholder="your@email.com"
            leftSection={<IconMail size={16} />}
            required
            mt="md"
            {...form.getInputProps('email')}
          />
          
          <PasswordInput
            label="Password"
            placeholder="Create a password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password')}
          />
          
          <PasswordInput
            label="Confirm password"
            placeholder="Confirm your password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password2')}
          />
          
          <Button fullWidth mt="xl" type="submit" disabled={isLoading}>
            Create account
          </Button>
        </form>
      </Paper>
    </Container>
  );
} 
### assets/js/components/Auth/Register.tsx END ###

### assets/js/components/Auth/PrivateRoute.tsx BEGIN ###
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingOverlay } from '@mantine/core';

interface PrivateRouteProps {
  children: React.ReactNode;
}

export function PrivateRoute({ children }: PrivateRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingOverlay visible />;
  }

  if (!isAuthenticated) {
    // Save the current location for redirect after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
} 
### assets/js/components/Auth/PrivateRoute.tsx END ###

### assets/js/components/Auth/Login.tsx BEGIN ###
import React, { useState } from 'react';
import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Text,
  Container,
  Group,
  Anchor,
  Center,
  Box,
  LoadingOverlay,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconUser, IconLock } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link, useLocation } from 'react-router-dom';

export function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const form = useForm({
    initialValues: {
      username: '',
      password: '',
    },
    validate: {
      username: (value: string) => (!value ? 'Username is required' : null),
      password: (value: string) => (!value ? 'Password is required' : null),
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    try {
      await login(values.username, values.password);
      // Always navigate to home page after login
      navigate('/', { replace: true });
    } catch (error) {
      // Error is handled in AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title
        ta="center"
        style={{
          fontFamily: `Greycliff CF, sans-serif`,
          fontWeight: 900,
        }}
      >
        Welcome back!
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Do not have an account yet?{' '}
        <Anchor component={Link} to="/register" size="sm">
          Create account
        </Anchor>
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />
        
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            label="Username"
            placeholder="Your username"
            leftSection={<IconUser size={16} />}
            required
            {...form.getInputProps('username')}
          />
          
          <PasswordInput
            label="Password"
            placeholder="Your password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password')}
          />
          
          <Group justify="apart" mt="lg">
            <Anchor component={Link} to="/forgot-password" size="sm">
              Forgot password?
            </Anchor>
          </Group>
          
          <Button fullWidth mt="xl" type="submit" disabled={isLoading}>
            Sign in
          </Button>
        </form>
      </Paper>
    </Container>
  );
} 
### assets/js/components/Auth/Login.tsx END ###

### assets/js/components/Chat/Chat.module.css BEGIN ###
.main {
  font-size: var(--mantine-font-size-md);
  height: 100vh;
  width: calc(100% - rem(250px));
  margin-left: auto;
}

.chatContainer {
  max-width: calc(51.25rem * var(--mantine-scale));
  height: 100%;
}

.chat {
  height: 100%;
}

.mdMessage p {
  margin: 0;
}

### assets/js/components/Chat/Chat.module.css END ###

### assets/js/components/Chat/Chat.tsx BEGIN ###
import {
  ActionIcon,
  Avatar,
  Button,
  Container,
  Group,
  LoadingOverlay,
  Paper,
  ScrollArea,
  Stack,
  Text,
  Textarea,
  Title,
  Tooltip,
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { ThreadsNav } from "../ThreadsNav/ThreadsNav";

import classes from "./Chat.module.css";
import { useCallback, useEffect, useRef, useState } from "react";
import { IconSend2, IconTrash } from "@tabler/icons-react";
import { getHotkeyHandler } from "@mantine/hooks";
import Markdown from "react-markdown";

import {
  useAssistant,
  useMessageList,
  useThreadList,
} from "django-ai-assistant-client";
import { Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

// Define types locally since they're not exported from the client
interface Thread {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

interface ThreadMessage {
  id: string;
  type: 'human' | 'ai';
  content: string;
  created_at: string;
}

function ChatMessage({
  message,
  deleteMessage,
}: {
  message: ThreadMessage;
  deleteMessage: ({ messageId }: { messageId: string }) => Promise<void>;
}) {
  const isUserMessage = message.type === "human";

  const DeleteButton = () => (
    <Tooltip label="Delete message" withArrow position="bottom">
      <ActionIcon
        variant="light"
        color="red"
        size="sm"
        onClick={async () => {
          await deleteMessage({ messageId: message.id });
        }}
        aria-label="Delete message"
      >
        <IconTrash style={{ width: "70%", height: "70%" }} stroke={1.5} />
      </ActionIcon>
    </Tooltip>
  );

  return (
    <Group
      gap="lg"
      align="flex-end"
      justify={isUserMessage ? "flex-end" : "flex-start"}
    >
      {!isUserMessage ? (
        <Avatar color="green" radius="xl">
          AI
        </Avatar>
      ) : null}

      {isUserMessage ? <DeleteButton /> : null}

      <Paper
        flex={1}
        maw="75%"
        shadow="none"
        radius="lg"
        p="xs"
        px="md"
        bg="var(--mantine-color-gray-0)"
      >
        <Group gap="md" justify="space-between" align="top">
          <Markdown className={classes.mdMessage}>{message.content}</Markdown>
        </Group>
      </Paper>

      {!isUserMessage ? <DeleteButton /> : null}
    </Group>
  );
}

function ChatMessageList({
  messages,
  deleteMessage,
}: {
  messages: ThreadMessage[];
  deleteMessage: ({ messageId }: { messageId: string }) => Promise<void>;
}) {
  if (messages.length === 0) {
    return <Text c="dimmed">No messages.</Text>;
  }

  return (
    <Stack gap="xl">
      {messages.map((message, index) => (
        <ChatMessage
          key={index}
          message={message}
          deleteMessage={deleteMessage}
        />
      ))}
    </Stack>
  );
}

export function Chat({ assistantId }: { assistantId: string }) {
  const [activeThread, setActiveThread] = useState<Thread | null>(null);
  const [inputValue, setInputValue] = useState<string>("");
  const { accessToken, isAuthenticated } = useAuth();

  // Log the current configuration
  useEffect(() => {
    console.log('[Chat] Component mounted/updated:', {
      assistantId,
      isAuthenticated,
      hasAccessToken: !!accessToken,
      // Try to check if the client has the config
      djangoAIAssistantConfig: (window as any).__DJANGO_AI_ASSISTANT_CONFIG__
    });
  }, [assistantId, isAuthenticated, accessToken]);

  const { fetchThreads, threads, createThread, deleteThread } = useThreadList({
    assistantId,
  });
  const {
    fetchMessages,
    messages,
    loadingFetchMessages,
    createMessage,
    loadingCreateMessage,
    deleteMessage,
    loadingDeleteMessage,
  } = useMessageList({ threadId: activeThread?.id?.toString() ?? null });

  const { fetchAssistant, assistant } = useAssistant({ assistantId });

  const loadingMessages =
    loadingFetchMessages || loadingCreateMessage || loadingDeleteMessage;
  const isThreadSelected = Boolean(activeThread);
  const isChatActive = activeThread && !loadingMessages;

  const scrollViewport = useRef<HTMLDivElement>(null);
  const scrollToBottom = useCallback(
    () =>
      // setTimeout is used because scrollViewport.current?.scrollHeight update is not
      // being triggered in time for the scrollTo method to work properly.
      setTimeout(
        () =>
          scrollViewport.current?.scrollTo({
            top: scrollViewport.current!.scrollHeight,
            behavior: "smooth",
          }),
        500
      ),
    [scrollViewport]
  );

  // Load threads and assistant details when component mounts and user is authenticated:
  useEffect(() => {
    async function loadAssistantAndThreads() {
      console.log('[Chat] loadAssistantAndThreads called:', {
        isAuthenticated,
        hasAccessToken: !!accessToken,
        accessTokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null,
        assistantId
      });
      
      if (!isAuthenticated || !accessToken) {
        console.log('[Chat] Not authenticated, skipping load');
        return; // Don't try to load if not authenticated
      }
      
      try {
        console.log('[Chat] Fetching assistant...');
        await fetchAssistant();
        console.log('[Chat] Assistant fetched successfully');
        
        console.log('[Chat] Fetching threads...');
        await fetchThreads();
        console.log('[Chat] Threads fetched successfully');
      } catch (error) {
        console.error('[Chat] Error loading assistant and threads:', error);
        if (error instanceof Error) {
          console.error('[Chat] Error details:', {
            message: error.message,
            stack: error.stack
          });
        }
      }
    }

    loadAssistantAndThreads();
  }, [fetchThreads, fetchAssistant, isAuthenticated, accessToken]);

  // Load messages when threadId changes:
  useEffect(() => {
    console.log('[Chat] Thread changed:', {
      assistantId,
      threadId: activeThread?.id,
      hasThread: !!activeThread
    });
    
    if (!assistantId) return;
    if (!activeThread) return;

    fetchMessages();
    scrollToBottom();
  }, [assistantId, activeThread?.id, fetchMessages]);

  async function handleCreateMessage() {
    console.log('[Chat] Creating message:', {
      hasThread: !!activeThread,
      messageLength: inputValue.length
    });
    
    if (!activeThread) return;

    await createMessage({
      assistantId,
      messageTextValue: inputValue,
    });

    setInputValue("");
    scrollToBottom();
  }

  return (
    <>
      <ThreadsNav
        threads={threads}
        selectedThreadId={activeThread?.id}
        selectThread={setActiveThread}
        createThread={createThread}
        deleteThread={deleteThread}
      />
      <main className={classes.main}>
        <Container className={classes.chatContainer}>
          <Stack className={classes.chat}>
            <Title mt="md" order={2}>
              Chat: {assistant?.name || "Loading…"}
            </Title>
            <ScrollArea
              pos="relative"
              type="auto"
              h="100%"
              px="xs"
              viewportRef={scrollViewport}
            >
              <LoadingOverlay
                visible={loadingMessages}
                zIndex={1000}
                overlayProps={{ blur: 2 }}
              />
              {isThreadSelected ? (
                <ChatMessageList
                  messages={messages || []}
                  deleteMessage={deleteMessage}
                />
              ) : (
                <Text c="dimmed">
                  Select or create a thread to start chatting.
                </Text>
              )}
            </ScrollArea>
            <Textarea
              mt="auto"
              mb="3rem"
              placeholder={
                isChatActive
                  ? "Enter user message… (Ctrl↵ to send)"
                  : "Please create or select a thread on the sidebar"
              }
              autosize
              minRows={2}
              disabled={!isChatActive}
              onChange={(e) => setInputValue(e.currentTarget.value)}
              value={inputValue}
              onKeyDown={getHotkeyHandler([["mod+Enter", handleCreateMessage]])}
              rightSection={
                <Button
                  variant="filled"
                  color="teal"
                  aria-label="Send message"
                  fz="xs"
                  rightSection={
                    <IconSend2
                      stroke={1.5}
                      style={{ width: "70%", height: "70%" }}
                    />
                  }
                  disabled={!isChatActive}
                  onClick={(e) => {
                    handleCreateMessage();
                    e.preventDefault();
                  }}
                >
                  Send
                </Button>
              }
              rightSectionWidth={120}
            />
          </Stack>
        </Container>
      </main>
    </>
  );
}

### assets/js/components/Chat/Chat.tsx END ###

### assets/js/components/PracticeScreen/PracticeScreen.tsx BEGIN ###
import { useAuth } from '../../contexts/AuthContext';

export function PracticeScreen() {
  const { threads, selectedThreadId, selectThread, createThread, deleteThread } =
    useThreads({
      assistantId: "python_practice_assistant",
    });
  const { sendMessage, isQuerying } = useAssistant({
    assistantId: "python_practice_assistant",
    threadId: selectedThreadId || undefined,
  });
  const [displayHistory, setDisplayHistory] = useState<DisplayMessage[]>([]);
  const [viewMode, setViewMode] = useState<'split' | 'full'>('split');
  const { user } = useAuth();

  // Custom debounce function
  const debounceTimeoutRef = React.useRef<NodeJS.Timeout | null>(null);

  // Auto-save current progress to localStorage
  const saveProgress = React.useCallback(() => {
    // Clear any existing timeout
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    // Set new timeout
    debounceTimeoutRef.current = setTimeout(() => {
      if (selectedThreadId && displayHistory.length > 0) {
        const progressKey = `practice_progress_${user?.id}_${selectedThreadId}`;
        localStorage.setItem(progressKey, JSON.stringify({
          displayHistory,
          timestamp: Date.now(),
        }));
        console.log('[PracticeScreen] Progress auto-saved');
      }
    }, 2000); // Save after 2 seconds of no activity
  }, [selectedThreadId, displayHistory, user?.id]);

  // Save progress whenever display history changes
  useEffect(() => {
    saveProgress();
  }, [displayHistory, saveProgress]);

  // Restore progress on mount or thread change
  useEffect(() => {
    if (selectedThreadId && user?.id) {
      const progressKey = `practice_progress_${user?.id}_${selectedThreadId}`;
      const savedProgress = localStorage.getItem(progressKey);
      
      if (savedProgress) {
        try {
          const { displayHistory: savedHistory } = JSON.parse(savedProgress);
          setDisplayHistory(savedHistory);
          console.log('[PracticeScreen] Progress restored from localStorage');
        } catch (error) {
          console.error('[PracticeScreen] Error restoring progress:', error);
        }
      }
    }
  }, [selectedThreadId, user?.id]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
    };
  }, []);

  // ... existing code ...
} 
### assets/js/components/PracticeScreen/PracticeScreen.tsx END ###

### assets/js/components/ThreadsNav/ThreadsNav.tsx BEGIN ###
import {
  Text,
  Group,
  ActionIcon,
  Tooltip,
  Loader,
  NavLink,
} from "@mantine/core";
import { useHover } from "@mantine/hooks";
import { IconPlus, IconTrash } from "@tabler/icons-react";
import classes from "./ThreadsNav.module.css";

import { Thread } from "django-ai-assistant-client";

export function ThreadsNav({
  threads,
  selectedThreadId,
  selectThread,
  createThread,
  deleteThread,
}: {
  threads: Thread[] | null;
  selectedThreadId: number | null | undefined;
  selectThread: (thread: Thread | null) => void;
  createThread: () => Promise<Thread>;
  deleteThread: ({ threadId }: { threadId: string }) => Promise<void>;
}) {
  const ThreadNavLink = ({ thread }: { thread: Thread }) => {
    const { hovered, ref } = useHover();
    const threadId = thread.id?.toString();

    return (
      <div ref={ref} key={thread.id}>
        <NavLink
          href="#"
          onClick={(event) => {
            selectThread(thread);
            event.preventDefault();
          }}
          label={thread.name}
          active={selectedThreadId === threadId}
          variant="filled"
          rightSection={
            hovered ? (
              <Tooltip label="Delete thread" withArrow>
                <ActionIcon
                  variant="light"
                  color="red"
                  size="sm"
                  onClick={async () => {
                    if (!threadId) return;
                    await deleteThread({ threadId });
                  }}
                  aria-label="Delete thread"
                >
                  <IconTrash
                    style={{ width: "70%", height: "70%" }}
                    stroke={1.5}
                  />
                </ActionIcon>
              </Tooltip>
            ) : null
          }
        />
      </div>
    );
  };

  const threadLinks = threads?.map((thread) => (
    <ThreadNavLink key={thread.id} thread={thread} />
  ));

  return (
    <nav className={classes.navbar}>
      <div className={classes.section}>
        <Group className={classes.threadsHeader} justify="space-between">
          <Text fw={500} c="dimmed">
            Threads
          </Text>
          <Tooltip label="Create thread" withArrow position="right">
            <ActionIcon
              variant="default"
              size="sm"
              onClick={async (e) => {
                const thread = await createThread();
                selectThread(thread);
                e.preventDefault();
              }}
            >
              <IconPlus style={{ width: "70%", height: "70%" }} stroke={1.5} />
            </ActionIcon>
          </Tooltip>
        </Group>

        <div className={classes.threads}>
          {threadLinks ? (
            threadLinks.length ? (
              threadLinks
            ) : (
              <Text className={classes.threadLinkInfo} c="dimmed">
                No threads found
              </Text>
            )
          ) : (
            <Loader className={classes.threadLinkInfo} color="blue" size="sm" />
          )}
        </div>
      </div>
    </nav>
  );
}

### assets/js/components/ThreadsNav/ThreadsNav.tsx END ###

### assets/js/components/ThreadsNav/ThreadsNav.module.css BEGIN ###
.navbar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  background-color: var(--mantine-color-body);
  width: rem(250px);
  padding: var(--mantine-spacing-md);
  padding-top: 0;
  display: flex;
  flex-direction: column;
  border-right: rem(1px) solid
    light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-4));
}

.section {
  margin-left: calc(var(--mantine-spacing-md) * -1);
  margin-right: calc(var(--mantine-spacing-md) * -1);
  margin-bottom: var(--mantine-spacing-md);

  &:not(:last-of-type) {
    border-bottom: rem(1px) solid
      light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-4));
  }
}

.threads {
  padding-left: calc(var(--mantine-spacing-md) - rem(6px));
  padding-right: calc(var(--mantine-spacing-md) - rem(6px));
  padding-bottom: var(--mantine-spacing-md);
}

.threadsHeader {
  padding-left: calc(var(--mantine-spacing-md) + rem(2px));
  padding-right: var(--mantine-spacing-md);
  margin-top: 1rem;
  margin-bottom: rem(5px);
}

.threadLinkInfo {
  padding: rem(8px) var(--mantine-spacing-xs);
  font-size: var(--mantine-font-size-sm);
}

### assets/js/components/ThreadsNav/ThreadsNav.module.css END ###

### assets/js/types/css.d.ts BEGIN ###
declare module "*.css" {
  interface IClassNames {
    [className: string]: string;
  }
  const classNames: IClassNames;
  export = classNames;
}

### assets/js/types/css.d.ts END ###

### assets/css/htmx_index.css BEGIN ###
#threads-container,
#messages-container {
  height: calc(100vh - 100px);
}

.main-container {
  max-width: 920px;
}

[data-loading] {
  display: none;
}

#messages-list li p {
  margin-bottom: 0;
}

### assets/css/htmx_index.css END ###

### apps/__init__.py BEGIN ###
# This file makes the apps directory a Python package 
### apps/__init__.py END ###

### apps/practice/grading_criteria.txt BEGIN ###
Grading Criteria (0-10):

**Grade 0 (Special Case)**
Reserved exclusively for:
- Empty code submissions
- Submissions containing only comments (no executable code)

**Grades 1-10 (For all submissions with executable code)**
Calculated using ceil(weighted_score * 10) where weighted_score is based on:

**Correctness (40%)
Based on static code analysis using AI evaluation of:
- Syntax and structure analysis
- Algorithm logic review
- Implementation completeness

Scoring (0-1 scale, converted to 4 points max):
- 0.8-1.0: Code structure sound, logic follows requirements, all major components implemented
- 0.5-0.7: Some logical issues or missing components, but core functionality present
- 0.2-0.4: Significant logical flaws or incomplete implementation
- 0.0-0.1: Major structural problems or completely incorrect approach

Note: Function names are not penalized for differences. REPL-like execution behavior is expected.

**Code Quality (30%)
Clean, readable code: 3 points
Adequate code: 1-2 points
Poor quality: 0 points

**Efficiency (20%)
Optimal solution: 2 points
Acceptable: 1 point
Inefficient: 0 points

**Sophistication (10%)
Good Sophistication: 1 point
Basic Sophistication: 0 points

Note: Any submission with executable code (even if it fails all tests) will receive at least grade 1.

-------------------------
Another option - from the project plan document:

**Correctness (%50)

**Efficiency (%25)

**Cleanliness (%15) (this is like Code Quality)

**Sophistication (%10)

I decided to go with the first option.
### apps/practice/grading_criteria.txt END ###

### apps/practice/tests.py BEGIN ###
from django.test import TestCase

# Create your tests here.

### apps/practice/tests.py END ###

### apps/practice/views.py BEGIN ###
import asyncio
from urllib import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
import random
import json
import time
import logging
import subprocess
import tempfile
import os
import signal
import sys
from datetime import datetime
import ast
from typing import Tuple

from apps.authentication.authentication import JWTOnlyAuthentication
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt
from .serializers import (
    UserStatsSerializer, QuestionSerializer, CodeSubmissionSerializer,
    CodeExecutionSerializer, GradeFeedbackSerializer, AttemptHistorySerializer,
    ManualLevelSerializer, LevelChangeSuggestionSerializer
)
from microsandbox import PythonSandbox
from .grading import PythonGradingEngine

logger = logging.getLogger(__name__)

# Flag to choose between execution methods
is_use_microsandbox = False


def execute_python_code(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code using the appropriate method based on is_use_microsandbox flag.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if is_use_microsandbox:
        return execute_python_code_with_micro_sandbox(code)
    else:
        return execute_python_code_with_timing(code)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get or create user progress statistics."""
    try:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        if created:
            logger.info(f"Created new UserProgress for user: {request.user.username}")
        
        serializer = UserStatsSerializer(user_progress)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return Response(
            {'error': 'Failed to retrieve user statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def set_manual_level(request):
    """Set user's manual difficulty level preference."""
    serializer = ManualLevelSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        level = serializer.validated_data['level']
        
        # Get or create user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Set the manual level
        success = user_progress.set_manual_level(level)
        
        if success:
            # Return updated user stats
            stats_serializer = UserStatsSerializer(user_progress)
            return Response({
                'message': f'Manual level set to {level}',
                'user_stats': stats_serializer.data
            })
        else:
            return Response(
                {'error': 'Invalid level value'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        logger.error(f"Error setting manual level: {e}")
        return Response(
            {'error': 'Failed to set manual level'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    """Get the next question based on user's manual level preference."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Check if user has a current question assigned
        if user_progress.current_question:
            # Return the current question
            serializer = QuestionSerializer(user_progress.current_question)
            stats_serializer = UserStatsSerializer(user_progress)
            
            logger.info(f"Returning current assigned question {user_progress.current_question.id} to user {request.user.username}")
            
            return Response({
                'question': serializer.data,
                'user_stats': stats_serializer.data
            })
        
        # No current question, assign a new one
        effective_level = user_progress.get_effective_level()
        
        # Get questions at the user's effective level
        questions = PythonProgrammingQuestion.objects.filter(
            difficulty_level=effective_level
        )
        
        # Get IDs of questions the user has already attempted
        attempted_question_ids = UserQuestionAttempt.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)
        
        # Filter out attempted questions
        available_questions = questions.exclude(id__in=attempted_question_ids)
        
        # If no new questions at current level, get any question at that level
        if not available_questions.exists():
            available_questions = questions
        
        # If still no questions, expand to nearby levels
        if not available_questions.exists():
            nearby_levels = [
                effective_level - 1,
                effective_level + 1
            ]
            available_questions = PythonProgrammingQuestion.objects.filter(
                difficulty_level__in=[l for l in nearby_levels if 1 <= l <= 5]
            ).exclude(id__in=attempted_question_ids)
        
        if available_questions.exists():
            # Select a random question
            question = random.choice(available_questions)
            
            # Assign the question to the user
            user_progress.assign_question(question)
            
            logger.info(f"Assigned new question {question.id} to user {request.user.username}")
            
            serializer = QuestionSerializer(question)
            stats_serializer = UserStatsSerializer(user_progress)
            
            return Response({
                'question': serializer.data,
                'user_stats': stats_serializer.data
            })
        else:
            return Response(
                {'error': 'No questions available at your level'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error getting next question: {e}")
        return Response(
            {'error': 'Failed to retrieve next question'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def submit_solution(request):
    logger.info(f"Submitting solution for user {request.user.username}")
    """Submit a solution for grading."""
    serializer = CodeSubmissionSerializer(data=request.data)
    logger.debug(f"DEBUG: Serializer created successfully, valid: {serializer.is_valid()}")
    
    if not serializer.is_valid():
        logger.error(f"DEBUG: Serializer validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        question_id = serializer.validated_data['question_id']
        code = serializer.validated_data['code']
        logger.debug(f"DEBUG: Extracted question_id={question_id}, code_length={len(code)}, code_preview='{code[:50]}...'")
        
        # Get the question
        question = PythonProgrammingQuestion.objects.get(id=question_id)
        
        # Get user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Validate that the user is submitting their currently assigned question
        if user_progress.current_question and user_progress.current_question.id != question_id:
            return Response(
                {'error': 'You can only submit the question currently assigned to you'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If no current question is assigned, assign this one (for backward compatibility)
        if not user_progress.current_question:
            user_progress.assign_question(question)
        
        # Execute the code to measure actual execution time
        _, _, execution_time = execute_python_code(code)
        
        # Create empty test_results dict since it's still expected by the grading engine
        # but not actually used in any evaluation
        test_results = {}
        
        # Grade the submission
        grading_engine = PythonGradingEngine()
        grade, feedback = grading_engine.grade_submission(
            code=code,
            question=question,
            test_results=test_results,
            execution_time=execution_time,
            user_id=request.user.id,
            username=request.user.username
        )
        
        # Save the attempt
        attempt = UserQuestionAttempt.objects.create(
            user=request.user,
            question=question,
            submitted_code=code,
            grade=grade,
            execution_time=execution_time,
            test_results=test_results,
            feedback=feedback
        )
        
        # Clear the current question since it's been submitted
        user_progress.clear_current_question()
        
        # Update user progress
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += grade
        
        # Increment correct answers count for grades 7-10
        if grade >= 7:
            user_progress.correct_answers_count += 1
        
        # Check for level change suggestion before updating counters
        level_suggestion = user_progress.check_level_change_suggestion(grade)
        
        # Update automatic level tracking (but don't use it for questions)
        user_progress.update_level(grade)
        
        level_changed = old_level != user_progress.current_level
        
        # Prepare response
        response_data = {
            'grade': grade,
            'feedback': feedback,
            'test_results': test_results,
            'execution_time': execution_time,
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None,
            'level_suggestion': level_suggestion
        }
        
        # Debug logging to verify all feedback is present
        logger.debug(f"Feedback being sent to frontend:")
        logger.debug(f"- Correctness: {feedback.get('correctness', {}).get('message', 'Not found')}")
        logger.debug(f"- Code Quality: {feedback.get('code_quality', {}).get('message', 'Not found')}")
        logger.debug(f"- Efficiency: {feedback.get('efficiency', {}).get('message', 'Not found')}")
        logger.debug(f"- Sophistication: {feedback.get('sophistication', {}).get('message', 'Not found')}")
        logger.debug(f"- Overall: {feedback.get('overall', 'Not found')}")
        
        response_serializer = GradeFeedbackSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data)
        else:
            return Response(response_data)
            
    except PythonProgrammingQuestion.DoesNotExist:
        return Response(
            {'error': 'Question not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error submitting solution: {e}")
        return Response(
            {'error': 'Failed to submit solution'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_attempt_history(request):
    """Get user's attempt history."""
    try:
        attempts = UserQuestionAttempt.objects.filter(
            user=request.user
        ).order_by('-attempted_at')[:20]  # Last 20 attempts
        
        serializer = AttemptHistorySerializer(attempts, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error getting attempt history: {e}")
        return Response(
            {'error': 'Failed to retrieve attempt history'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def clear_user_progress(request):
    """Clear all user progress data including UserProgress and UserQuestionAttempt records."""
    try:
        user = request.user
        logger.info(f"Clearing progress for user: {user.username} (ID: {user.id})")
        
        # Delete all UserQuestionAttempt records for this user
        attempts_deleted, _ = UserQuestionAttempt.objects.filter(user=user).delete()
        
        # Clear current question from UserProgress before deleting
        user_progress = UserProgress.objects.filter(user=user).first()
        if user_progress:
            user_progress.clear_current_question()
        
        # Delete UserProgress record for this user (if exists)
        progress_deleted, _ = UserProgress.objects.filter(user=user).delete()
        
        logger.info(f"Cleared progress for user {user.username}: "
                   f"{attempts_deleted} attempts, {progress_deleted} progress records")
        
        return Response({
            'message': 'Clear Progress completed',
            'attempts_cleared': attempts_deleted,
            'progress_cleared': progress_deleted
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error clearing user progress: {e}")
        return Response(
            {'error': 'Failed to clear user progress'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def abandon_current_question(request):
    """Allow user to abandon their current question, recording it as a failed attempt."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Check if user has a current question
        if not user_progress.current_question:
            return Response(
                {'error': 'No current question to abandon'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_question = user_progress.current_question
        
        # Record the abandonment as a failed attempt with grade 0
        attempt = UserQuestionAttempt.objects.create(
            user=request.user,
            question=current_question,
            submitted_code="",  # Empty code for abandoned question
            grade=0,  # Grade 0 for abandoned question
            execution_time=0.0,
            test_results={},
            feedback={
                'overall': 'Question abandoned by user',
                'correctness': {'score': 0, 'message': 'Question was abandoned'},
                'code_quality': {'score': 0, 'message': 'No code submitted'},
                'efficiency': {'score': 0, 'message': 'No code submitted'},
                'sophistication': {'score': 0, 'message': 'No code submitted'}
            }
        )
        
        # Update user progress statistics
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += 0  # Add 0 to score
        
        # Check for level change suggestion
        level_suggestion = user_progress.check_level_change_suggestion(0)
        
        # Update automatic level tracking
        user_progress.update_level(0)
        
        # Clear the current question
        user_progress.clear_current_question()
        
        level_changed = old_level != user_progress.current_level
        
        logger.info(f"User {request.user.username} abandoned question {current_question.id}")
        
        return Response({
            'message': 'Question abandoned successfully',
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None,
            'level_suggestion': level_suggestion
        })
        
    except Exception as e:
        logger.error(f"Error abandoning current question: {e}")
        return Response(
            {'error': 'Failed to abandon current question'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_python_code(request):
    """
    Execute Python code on the backend and return the output without submission (for testing)
    """
    code = request.data.get('code', '')
    
    # Execute the code and get output, error, and execution time (empty code is allowed)
    output, error, execution_time = execute_python_code(code)
    
    # Return appropriate response based on error status
    if error and 'timed out' in error:
        return Response({
            'output': output,
            'error': error,
            'execution_time': execution_time
        }, status=status.HTTP_408_REQUEST_TIMEOUT)
    
    return Response({
        'output': output,
        'error': error,
        'execution_time': execution_time
    })

def execute_python_code_with_micro_sandbox(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code using microsandbox and return output, error, and execution time.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if os.environ.get('SKIP_CODE_EXECUTION') == 'True':
        return 'Code execution is disabled in this environment', None, 0.1
    
    try:
        # Process the code to handle expressions like REPL
        processed_code = process_code_for_repl(code)
        
        # Measure execution time
        start_time = time.time()
        
        try:
            # Execute using microsandbox with timeout
            async def run_with_sandbox():
                async with PythonSandbox.create(name=f"sandbox_{int(time.time())}") as sandbox:
                    # Set a 10-second timeout for the entire execution
                    async with asyncio.timeout(10):
                        exec_result = await sandbox.run(processed_code)
                        output = await exec_result.output()
                        return output, None
            
            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                output, error = loop.run_until_complete(run_with_sandbox())
            finally:
                loop.close()
            
            # Calculate execution time in seconds
            execution_time = time.time() - start_time
            
            return output, error, execution_time
            
        except asyncio.TimeoutError:
            return '', 'Code execution timed out (10 seconds limit)', 10.0
            
    except Exception as e:
        return '', f'Execution error: {str(e)}', 0.1

def execute_python_code_with_timing(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code and return output, error, and execution time.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if os.environ.get('SKIP_CODE_EXECUTION') == 'True':
        return 'Code execution is disabled in this environment', None, 0.1
    
    try:
        # Process the code to handle expressions like REPL
        processed_code = process_code_for_repl(code)
        
        # Create a temporary file for the Python code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(processed_code)
            temp_file_path = temp_file.name
        
        try:
            # Measure execution time
            start_time = time.time()
            
            # Execute the Python code with timeout
            result = subprocess.run([
                sys.executable, temp_file_path
            ], 
            capture_output=True, 
            text=True, 
            timeout=10,  # 10 second timeout
            cwd=tempfile.gettempdir()  # Run in temp directory for security
            )
            
            # Calculate execution time in seconds
            execution_time = time.time() - start_time
            
            output = result.stdout
            error = result.stderr if result.returncode != 0 else None
            
            return output, error, execution_time
            
        except subprocess.TimeoutExpired:
            return '', 'Code execution timed out (10 seconds limit)', 10.0
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        return '', f'Execution error: {str(e)}', 0.1


def process_code_for_repl(code: str) -> str:
    """
    Process code to make it behave like a REPL, automatically printing expressions.
    """
    # Handle empty code
    if not code or not code.strip():
        return ''
    
    lines = code.strip().split('\n')
    if not lines:
        return code
    
    try:
        # Try to parse the entire code first
        tree = ast.parse(code)
        
        # If the last statement is an expression, wrap it with print()
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            # Split code into all lines except the last expression
            all_but_last = '\n'.join(lines[:-1])
            last_line = lines[-1].strip()
            
            # Check if the last line is likely an expression (not an assignment or statement)
            try:
                # Parse just the last line
                last_tree = ast.parse(last_line)
                if last_tree.body and isinstance(last_tree.body[0], ast.Expr):
                    # It's an expression, wrap it with conditional print to skip None values
                    if all_but_last.strip():
                        return f"{all_but_last}\n_expr_result = {last_line}\nif _expr_result is not None:\n    print(_expr_result)"
                    else:
                        return f"_expr_result = {last_line}\nif _expr_result is not None:\n    print(_expr_result)"
            except:
                pass
        
        # For single-line expressions
        if len(lines) == 1:
            try:
                # Try to parse as an expression
                ast.parse(lines[0], mode='eval')
                # It's a valid expression, wrap with conditional print
                return f"_expr_result = {lines[0]}\nif _expr_result is not None:\n    print(_expr_result)"
            except:
                # Not a simple expression, return as is
                pass
                
    except SyntaxError:
        # If there's a syntax error, let it fail naturally during execution
        pass
    
    return code

### apps/practice/views.py END ###

### apps/practice/grading.py BEGIN ###
import ast
import re
import json
import math
import logging
from typing import Dict, List, Tuple, Any
from apps.api import ClaudeService
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
grading_logger = logging.getLogger('grading_logger')


class PythonGradingEngine:
    """
    Grades Python code submissions on a scale of 0-10.
    
    Grade 0 is reserved for:
    - Empty code submissions
    - Submissions containing only comments (no executable code)
    
    Grades 1-10 are calculated based on:
    - Correctness (40%): 4 points max
    - Code Quality (30%): 3 points max  
    - Efficiency (20%): 2 points max
    - Sophistication (10%): 1 point max
    """
    
    def __init__(self):
        self.total_points = 10
        self.claude_service = ClaudeService()
        
    def grade_submission(
        self, 
        code: str, 
        question: 'PythonProgrammingQuestion',
        test_results: Dict[str, Any],
        execution_time: float = None,
        user_id: int = None,
        username: str = None
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Grade a code submission and return grade (0-10) and detailed feedback.
        
        Grade 0 is returned for empty code or code with only comments.
        Grades 1-10 are calculated using weighted scoring with ceil function.
        
        Args:
            code: The submitted Python code
            question: The PythonProgrammingQuestion object
            test_results: Results from running test cases
            execution_time: Time taken to execute the code
            user_id: User ID for logging purposes
            username: Username for logging purposes
            
        Returns:
            Tuple of (grade, feedback_dict)
        """
        # Log grading start
        grading_logger.info(f"{'='*80}")
        grading_logger.info(f"GRADING START - User: {username} (ID: {user_id})")
        grading_logger.info(f"Question ID: {question.id}")
        grading_logger.info(f"Question Instruction: {question.instruction}")
        grading_logger.info(f"Question Input: {question.input}")
        grading_logger.info(f"Expected Output: {question.output}")
        grading_logger.info(f"Difficulty Level: {question.difficulty_level}")
        grading_logger.info(f"Execution Time: {execution_time:.3f}s")
        grading_logger.info(f"Submitted Code:\n{code}")
        grading_logger.info(f"{'-'*80}")
        feedback = {
            'correctness': {},
            'code_quality': {},
            'efficiency': {},
            'sophistication': {},
            'overall': ''
        }
        
        # Check for empty code or comments-only code
        if self._is_empty_or_comments_only(code):
            feedback['overall'] = self._generate_overall_feedback(
                0, 0.0, 0.0, 0.0, 0.0, is_empty_or_comments_only=True
            )
            feedback['correctness'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['code_quality'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['efficiency'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['sophistication'] = {'score': 0, 'message': 'No code to evaluate.'}
            
            # Log grade 0 results
            grading_logger.info(f"Empty or comments-only code detected")
            grading_logger.info(f"Correctness Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Code Quality Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Efficiency Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Sophistication Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"{'-'*80}")
            grading_logger.info(f"Weighted Score: 0.0000")
            grading_logger.info(f"Final Grade: 0/10")
            grading_logger.info(f"Overall Feedback: {feedback['overall']}")
            grading_logger.info(f"GRADING END - User: {username} (ID: {user_id})")
            grading_logger.info(f"{'='*80}\n")
            
            return 0, feedback
        
        # Calculate individual scores (0-1 scale)
        correctness_score = self._evaluate_correctness(code, question, feedback)
        grading_logger.info(f"Correctness Score: {correctness_score:.2f} - {feedback['correctness'].get('message', 'No message')}")
        
        # If correctness is zero, all other scores should be zero
        if correctness_score == 0:
            quality_score = 0
            efficiency_score = 0
            sophistication_score = 0
            
            # Set appropriate feedback messages for zero scores
            feedback['code_quality'] = {
                'score': 0,
                'message': 'Code quality cannot be evaluated when correctness is zero.',
                'issues': ['Code must be correct before quality can be assessed']
            }
            feedback['efficiency'] = {
                'score': 0,
                'message': 'Efficiency cannot be evaluated when correctness is zero.',
                'inefficiencies': ['Code must be correct before efficiency can be assessed'],
                'suggestions': []
            }
            feedback['sophistication'] = {
                'score': 0,
                'message': 'Sophistication cannot be evaluated when correctness is zero.',
                'areas_for_improvement': ['Code must be correct before sophistication can be assessed'],
                'advanced_techniques': []
            }
            
            grading_logger.info(f"Code Quality Score: 0.00 - Code quality cannot be evaluated when correctness is zero.")
            grading_logger.info(f"Efficiency Score: 0.00 - Efficiency cannot be evaluated when correctness is zero.")
            grading_logger.info(f"Sophistication Score: 0.00 - Sophistication cannot be evaluated when correctness is zero.")
        else:
            # Normal evaluation for non-zero correctness
            # Code quality can run immediately (no API call)
            quality_score = self._evaluate_code_quality(code, question, feedback)
            grading_logger.info(f"Code Quality Score: {quality_score:.2f} - {feedback['code_quality'].get('message', 'No message')}")
            
            # Run efficiency and sophistication evaluations in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both API calls
                future_efficiency = executor.submit(
                    self._evaluate_efficiency, code, execution_time, question, feedback
                )
                future_sophistication = executor.submit(
                    self._evaluate_sophistication, code, question, feedback
                )
                
                # Wait for both to complete
                efficiency_score = future_efficiency.result()
                sophistication_score = future_sophistication.result()
            
            grading_logger.info(f"Efficiency Score: {efficiency_score:.2f} - {feedback['efficiency'].get('message', 'No message')}")
            grading_logger.info(f"Sophistication Score: {sophistication_score:.2f} - {feedback['sophistication'].get('message', 'No message')}")
        
        # Calculate weighted_score (0-1 scale)
        weighted_score = (
            correctness_score * 0.4 +
            quality_score * 0.3 +
            efficiency_score * 0.2 +
            sophistication_score * 0.1
        )
        
        # Calculate grade (1-10) using ceil function
        # Any positive weighted score results in at least grade 1
        # If all scores are zero, grade should be zero
        if weighted_score > 0:
            grade = math.ceil(weighted_score * 10)
        else:
            grade = 0  # Grade 0 when all aspects score zero
        
        # Generate overall feedback
        feedback['overall'] = self._generate_overall_feedback(
            grade, correctness_score, quality_score, 
            efficiency_score, sophistication_score, 
            is_empty_or_comments_only=False
        )
        
        # Log final results
        grading_logger.info(f"{'-'*80}")
        grading_logger.info(f"Weighted Score: {weighted_score:.4f}")
        grading_logger.info(f"Final Grade: {grade}/10")
        grading_logger.info(f"Overall Feedback: {feedback['overall']}")
        grading_logger.info(f"GRADING END - User: {username} (ID: {user_id})")
        grading_logger.info(f"{'='*80}\n")
        
        return grade, feedback
    
    def _evaluate_correctness(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate correctness using Claude API for static code analysis (0-1 scale)."""
        try:
            # Create prompt for Claude to evaluate correctness
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output"],
                template="""
Please evaluate the correctness of the following Python code submission based on static analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}

Submitted Code:
```python
{code}
```

**IMPORTANT GRADING CONSIDERATIONS**:
1. **Function Names**: DO NOT penalize for function name differences. Students cannot see the expected solution, so as long as the function name is meaningful and descriptive of its functionality, it should NOT affect the correctness score.

2. **REPL-like Execution**: The code execution simulates REPL (Read-Eval-Print Loop) behavior. The system automatically wraps the last expression with a print statement if it evaluates to a non-None value. This is EXPECTED behavior and should NOT be penalized. For example:
   - `calculate_sum(5, 3)` at the end will automatically print the result
   - `5 + 3` as the last line will automatically print `8`
   - `my_variable` at the end will print its value (if not None)
   - This is functionally equivalent to having an explicit print() statement

DO NOT mark the code as having "no output" or penalize for "missing print statements" if the solution relies on this automatic printing behavior. The code is correct if the last expression produces the expected output value.

Evaluate the code based on these criteria:

1. **Syntax and Structure Analysis**:
   - Check for proper Python syntax (indentation, colons, parentheses)
   - Verify function definitions include proper parameters and return statements
   - Examine conditional statements for logical completeness
   - Look for proper loop termination conditions

2. **Algorithm Logic Review**:
   - Trace through the code logic manually with sample inputs
   - Verify that the algorithm follows the problem requirements
   - Check for proper variable initialization and usage
   - Examine control flow paths to ensure all scenarios are handled

3. **Correctness Score Guidelines**:
   - 0.8-1.0: Code structure appears sound, logic follows requirements, all major components implemented
   - 0.5-0.7: Some logical issues or missing components, but core functionality present
   - 0.2-0.4: Significant logical flaws or incomplete implementation
   - 0.0-0.1: Major structural problems or completely incorrect approach

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation of your analysis>",
    "issues": ["<list of specific issues found, if any>"],
    "strengths": ["<list of strengths in the implementation>"]
}}
"""
            )
            
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output
            )
            # ...

            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "issues": ["Could not parse evaluation"],
                        "strengths": []
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "issues": ["Could not parse evaluation"],
                    "strengths": []
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Correctness Analysis: {result.get('analysis', 'No analysis')}")
            if result.get('issues'):
                grading_logger.debug(f"Issues Found: {result.get('issues', [])}")
            if result.get('strengths'):
                grading_logger.debug(f"Strengths: {result.get('strengths', [])}")
            
            # Generate feedback message
            if score >= 0.9:
                message = f"Excellent! Your code logic appears correct and well-structured."
            elif score >= 0.7:
                message = f"Good job! Your code shows solid understanding with minor issues."
            elif score >= 0.5:
                message = f"Partial success. Your code has the right idea but needs improvements."
            elif score >= 0.3:
                message = f"Keep trying! Your code has some logical issues that need fixing."
            else:
                message = f"Review the problem requirements carefully and restructure your approach."
            
            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['correctness'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'issues': result.get('issues', []),
                'strengths': result.get('strengths', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating correctness with Claude API: {e}")
            feedback['correctness'] = {
                'score': 0.5,
                'message': 'Could not evaluate correctness automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _evaluate_code_quality(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code quality (0-1 scale) adjusted for difficulty level."""
        quality_score = 1.0
        issues = []
        difficulty_level = question.difficulty_level
        
        try:
            # Parse the code AST
            tree = ast.parse(code)
            
            # Check for functions (only for appropriate difficulty levels)
            if difficulty_level >= 2:  # Only expect functions for Easy and above
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                if not functions and len(code.split('\n')) > 10:  # Only penalize if code is long enough to warrant functions
                    if difficulty_level == 2:
                        quality_score -= 0.1  # Smaller penalty for Easy level
                        issues.append("Consider using functions to organize your code")
                    else:
                        quality_score -= 0.2  # Larger penalty for Medium and above
                        issues.append("Use functions to organize your code better")
            
            # Check for meaningful variable names (adjusted by level)
            if self._has_poor_variable_names(code):
                if difficulty_level == 1:
                    quality_score -= 0.1  # Smaller penalty for beginners
                    issues.append("Try to use more descriptive variable names")
                else:
                    quality_score -= 0.2
                    issues.append("Use more descriptive variable names")
            
            # Check for comments (only for appropriate difficulty levels)
            if difficulty_level >= 2:  # Don't expect comments for very basic problems
                if code.count('#') < 1 and code.count('"""') < 1 and len(code.split('\n')) > 5:
                    quality_score -= 0.1
                    issues.append("Add comments to explain your logic")
            
            # Check line length (less strict for beginners)
            if difficulty_level >= 3:
                long_lines = [line for line in code.split('\n') if len(line) > 80]
                if len(long_lines) > 3:
                    quality_score -= 0.1
                    issues.append("Some lines are too long (>80 characters)")
            else:
                # More lenient for beginners
                long_lines = [line for line in code.split('\n') if len(line) > 100]
                if len(long_lines) > 5:
                    quality_score -= 0.05
                    issues.append("Try to keep lines shorter for better readability")
            
            # Check for duplicate code (adjusted by level)
            if self._has_duplicate_code(code):
                if difficulty_level >= 2:
                    quality_score -= 0.2
                    issues.append("Avoid code duplication - use functions or loops")
                else:
                    quality_score -= 0.1
                    issues.append("Try to avoid repeating the same code")
                
        except SyntaxError:
            quality_score = 0.1
            issues = ["Syntax error in code"]
        
        quality_score = max(0, quality_score)
        
        # Generate level-appropriate feedback messages
        if difficulty_level == 1:  # Very Easy
            if quality_score >= 0.9:
                message = "Great code quality for a beginner problem!"
            elif quality_score >= 0.7:
                message = "Good code quality. Keep practicing!"
            else:
                message = "Your code works but could be cleaner."
        elif difficulty_level == 2:  # Easy
            if quality_score >= 0.9:
                message = "Excellent code quality! Well organized."
            elif quality_score >= 0.7:
                message = "Good code quality. Consider the suggestions."
            else:
                message = "Code quality needs some improvement."
        else:  # Medium and above
            if quality_score >= 0.9:
                message = "Excellent code quality!"
            elif quality_score >= 0.7:
                message = "Good code quality."
            else:
                message = "Code quality needs improvement."
        
        feedback['code_quality'] = {
            'score': quality_score,
            'issues': issues,
            'message': message
        }
        
        return quality_score
    
    def _evaluate_efficiency(self, code: str, execution_time: float, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code efficiency using Claude API for context-aware assessment (0-1 scale)."""
        try:
            # Get difficulty level from question
            difficulty_level = question.difficulty_level
            
            # Create prompt for Claude to evaluate efficiency
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output", "difficulty_level"],
                template="""
Please evaluate the efficiency of the following Python code submission based on static performance analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}
Difficulty Level: {difficulty_level} (1=Very Easy, 2=Easy, 3=Medium, 4=Hard, 5=Very Hard)

Submitted Code:
```python
{code}
```

**Efficiency Assessment (20% weight) - Static Performance Analysis**

**IMPORTANT: Adjust efficiency expectations based on the difficulty level.**

**Level-Specific Efficiency Guidelines:**

**Level 1 (Very Easy)**: For basic problems:
- Simple, direct solutions are PERFECTLY FINE
- DO NOT penalize for using simple loops when appropriate
- DO NOT expect optimizations like sets or dictionaries
- Focus: Does the code avoid obviously wasteful operations?

**Level 2 (Easy)**: For fundamental problems:
- Basic efficiency awareness (avoiding unnecessary loops)
- Simple optimizations are good but not required
- DO NOT penalize for not using advanced data structures
- Focus: Are there obvious inefficiencies that a beginner should avoid?

**Level 3 (Medium)**: For intermediate problems:
- Expect awareness of time complexity
- Appropriate data structure choices (lists vs sets vs dicts)
- Basic algorithm optimization
- Focus: Is the algorithm choice reasonable for the problem?

**Level 4 (Hard)**: For advanced problems:
- Expect optimal algorithm selection
- Advanced data structure usage
- Consideration of space-time tradeoffs
- Focus: Is this an efficient solution for production code?

**Level 5 (Very Hard)**: For expert problems:
- Expect professional-level optimization
- Advanced algorithmic techniques
- Consideration of real-world constraints
- Focus: Is this optimized for scale and performance?

**General Evaluation Criteria:**

1. **Algorithm Complexity Assessment**:
   - Time Complexity Analysis: Count nested loops, recursive calls
   - Single loops: O(n) - generally efficient
   - Nested loops: O(n²) - acceptable for small datasets
   - Triple nesting or higher: potentially inefficient

2. **Specific Efficiency Indicators to Penalize (adjust severity by level)**:
   - **Excessive Nested Loops**: Only penalize if exceeding what's needed for the problem AND the difficulty level
   - **'in' operator inside loops**: Only penalize at level 3+ and if it significantly impacts performance
   - Inefficient data structure choices: Only penalize at level 3+ 
   - Redundant computations: Severity depends on difficulty level
   - Excessive string concatenation in loops: Only penalize if severe

3. **Efficiency Bonuses (only for appropriate difficulty levels)**:
   - **Efficient Data Structures**: Only bonus at level 3+
   - Smart algorithmic choices: Bonus scaled by difficulty level
   - Space-time tradeoff awareness: Only at level 4+

4. **Context-Aware Evaluation**:
   - Consider the problem's requirements and expected input size
   - DO NOT over-penalize simple solutions for simple problems
   - DO NOT expect advanced optimizations for beginner problems

**Efficiency Scoring Guidelines by Level**:

Level 1-2 (Very Easy/Easy):
- 0.8-1.0: Direct solution without obviously wasteful operations
- 0.5-0.7: Some unnecessary operations but functional
- 0.0-0.4: Clearly inefficient even for a beginner

Level 3 (Medium):
- 0.8-1.0: Good algorithm choice with appropriate data structures
- 0.5-0.7: Reasonable approach with minor inefficiencies
- 0.0-0.4: Poor algorithm choice or significant inefficiencies

Level 4-5 (Hard/Very Hard):
- 0.8-1.0: Optimal or near-optimal implementation
- 0.5-0.7: Good approach with optimization opportunities
- 0.0-0.4: Suboptimal approach for this complexity level

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation appropriate to difficulty level>",
    "time_complexity": "<estimated time complexity e.g. O(n), O(n²)>",
    "inefficiencies": ["<list of level-appropriate inefficiencies, if any>"],
    "suggestions": ["<list of level-appropriate optimization suggestions>"],
    "penalties_applied": ["<list of penalties appropriate to difficulty level>"],
    "bonuses_applied": ["<list of bonuses if appropriate for level>"]
}}
"""
            )
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output,
                difficulty_level=difficulty_level
            )
            # ...
            
            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "time_complexity": "Unknown",
                        "inefficiencies": ["Could not parse evaluation"],
                        "suggestions": [],
                        "penalties_applied": [],
                        "bonuses_applied": []
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "time_complexity": "Unknown",
                    "inefficiencies": ["Could not parse evaluation"],
                    "suggestions": [],
                    "penalties_applied": [],
                    "bonuses_applied": []
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Efficiency Analysis: {result.get('analysis', 'No analysis')}")
            grading_logger.debug(f"Time Complexity: {result.get('time_complexity', 'Unknown')}")
            if result.get('inefficiencies'):
                grading_logger.debug(f"Inefficiencies: {result.get('inefficiencies', [])}")
            if result.get('suggestions'):
                grading_logger.debug(f"Optimization Suggestions: {result.get('suggestions', [])}")
            if result.get('penalties_applied'):
                grading_logger.debug(f"Penalties Applied: {result.get('penalties_applied', [])}")
            if result.get('bonuses_applied'):
                grading_logger.debug(f"Bonuses Applied: {result.get('bonuses_applied', [])}")
            
            # Generate feedback message
            if score >= 0.8:
                message = f"Highly efficient solution! Time complexity: {result.get('time_complexity', 'N/A')}."
            elif score >= 0.5:
                message = f"Reasonable efficiency. Time complexity: {result.get('time_complexity', 'N/A')}."
            elif score >= 0.2:
                message = f"Some inefficiencies present. Time complexity: {result.get('time_complexity', 'N/A')}."
            else:
                message = f"Efficiency needs improvement. Time complexity: {result.get('time_complexity', 'N/A')}."
            
            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['efficiency'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'time_complexity': result.get('time_complexity', 'Unknown'),
                'inefficiencies': result.get('inefficiencies', []),
                'suggestions': result.get('suggestions', []),
                'penalties_applied': result.get('penalties_applied', []),
                'bonuses_applied': result.get('bonuses_applied', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating efficiency with Claude API: {e}")
            feedback['efficiency'] = {
                'score': 0.5,
                'message': 'Could not evaluate efficiency automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _evaluate_sophistication(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code sophistication including edge case handling using Claude API (0-1 scale)."""
        try:
            # Get difficulty level from question
            difficulty_level = question.difficulty_level
            
            # Create prompt for Claude to evaluate sophistication
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output", "difficulty_level"],
                template="""
Please evaluate the sophistication of the following Python code submission based on static analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}
Difficulty Level: {difficulty_level} (1=Very Easy, 2=Easy, 3=Medium, 4=Hard, 5=Very Hard)

Submitted Code:
```python
{code}
```

**IMPORTANT: Adjust your sophistication expectations based on the difficulty level of the question.**

Code sophistication should be evaluated relative to what's reasonable for the difficulty level:

**Level 1 (Very Easy - Beginner)**: For basic syntax problems, sophistication means:
- Clean, readable code with meaningful variable names (e.g., 'counter' instead of 'i' when appropriate)
- Basic code organization (not everything in one line unless appropriate)
- Simple comments for clarity (if the problem warrants it)
- DO NOT expect: functions, classes, error handling, advanced features, or over-engineering
- Example improvements: Better variable names, simple comments, clean formatting

**Level 2 (Easy - Fundamental)**: For basic programming problems, sophistication means:
- Using functions for code organization (when appropriate)
- Basic input validation for obvious edge cases
- Clear variable and function names
- Basic documentation/comments
- DO NOT expect: OOP, advanced patterns, complex error handling, generators
- Example improvements: Function usage, basic validation, simple docstrings

**Level 3 (Medium - Intermediate)**: For intermediate problems, sophistication means:
- Good use of Python features (list comprehensions, appropriate data structures)
- Proper error handling for common cases
- Well-structured code with clear separation of concerns
- Some consideration of efficiency
- DO NOT expect: Design patterns, async programming, advanced OOP
- Example improvements: List comprehensions, try-except blocks, better algorithms

**Level 4 (Hard - Advanced)**: For complex problems, sophistication means:
- Appropriate use of OOP or functional programming concepts
- Comprehensive error handling
- Good algorithm choices and data structures
- Clear architecture and design
- Edge case handling
- Example improvements: Class design, advanced data structures, optimization

**Level 5 (Very Hard - Expert)**: For professional-level problems, sophistication means:
- Professional-grade code architecture
- Advanced Python features (decorators, generators, async)
- Comprehensive testing considerations
- Performance optimization
- Design patterns where appropriate
- Example improvements: Architecture patterns, advanced optimizations, scalability

**Evaluation Guidelines**:
- Award points for sophistication APPROPRIATE TO THE DIFFICULTY LEVEL
- DO NOT penalize beginners for not using advanced features
- DO NOT suggest over-engineering simple problems
- Focus on what would be the NEXT reasonable improvement for someone at that level

**Sophistication Scoring Based on Difficulty Level**:

For Level 1 (Very Easy):
- 0.8-1.0: Clean, readable code with good variable names and basic organization
- 0.5-0.7: Functional but could use better naming or organization
- 0.0-0.4: Poor organization, unclear variable names, or unnecessarily complex

For Level 2 (Easy):
- 0.8-1.0: Well-organized with functions, basic validation, clear naming
- 0.5-0.7: Some organization, missing some basic best practices
- 0.0-0.4: No functions where needed, poor structure, no validation

For Level 3 (Medium):
- 0.8-1.0: Good use of Python features, proper error handling, efficient approach
- 0.5-0.7: Some advanced features used, basic error handling
- 0.0-0.4: Missing opportunities for Python features, no error handling

For Level 4 (Hard):
- 0.8-1.0: Strong architecture, comprehensive error handling, optimal algorithms
- 0.5-0.7: Good structure, some advanced concepts, decent error handling
- 0.0-0.4: Weak architecture, minimal error handling, suboptimal approach

For Level 5 (Very Hard):
- 0.8-1.0: Professional-grade code with advanced features and optimization
- 0.5-0.7: Good implementation with some advanced concepts
- 0.0-0.4: Basic implementation lacking professional considerations

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation appropriate to the difficulty level>",
    "advanced_techniques": ["<list of techniques used that are appropriate for this level>"],
    "edge_cases_handled": ["<list of edge cases handled, if expected at this level>"],
    "areas_for_improvement": ["<list of LEVEL-APPROPRIATE improvements>"]
}}
"""
            )
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output,
                difficulty_level=difficulty_level
            )
            # ...
            
            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "advanced_techniques": [],
                        "edge_cases_handled": [],
                        "areas_for_improvement": ["Could not parse evaluation"]
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "advanced_techniques": [],
                    "edge_cases_handled": [],
                    "areas_for_improvement": ["Could not parse evaluation"]
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Sophistication Analysis: {result.get('analysis', 'No analysis')}")
            if result.get('advanced_techniques'):
                grading_logger.debug(f"Techniques Used: {result.get('advanced_techniques', [])}")
            if result.get('edge_cases_handled'):
                grading_logger.debug(f"Edge Cases Handled: {result.get('edge_cases_handled', [])}")
            if result.get('areas_for_improvement'):
                grading_logger.debug(f"Areas for Improvement: {result.get('areas_for_improvement', [])}")
            
            # Generate feedback message based on difficulty level
            if difficulty_level == 1:  # Very Easy
                if score >= 0.8:
                    message = "Excellent! Your code is clean, readable, and well-organized for a beginner problem."
                elif score >= 0.5:
                    message = "Good job! Your code works well. Consider using more descriptive variable names."
                else:
                    message = "Your solution works, but could be cleaner. Focus on readability and organization."
            elif difficulty_level == 2:  # Easy
                if score >= 0.8:
                    message = "Great work! Your code is well-structured with good use of functions and basic best practices."
                elif score >= 0.5:
                    message = "Good effort! Consider organizing your code with functions and adding basic validation."
                else:
                    message = "Your code works but needs better structure. Try using functions to organize your logic."
            elif difficulty_level == 3:  # Medium
                if score >= 0.8:
                    message = "Excellent! You've used Python features effectively with good error handling and structure."
                elif score >= 0.5:
                    message = "Good implementation! Consider using more Python features like list comprehensions or better error handling."
                else:
                    message = "Your solution could benefit from Python's built-in features and better error handling."
            elif difficulty_level == 4:  # Hard
                if score >= 0.8:
                    message = "Outstanding! Your code shows strong architecture, comprehensive error handling, and optimal design."
                elif score >= 0.5:
                    message = "Good advanced implementation! Consider improving error handling or algorithm optimization."
                else:
                    message = "For this complexity level, focus on better architecture and comprehensive error handling."
            else:  # Level 5 - Very Hard
                if score >= 0.8:
                    message = "Professional-grade code! Excellent use of advanced features and optimization."
                elif score >= 0.5:
                    message = "Strong implementation! Consider additional optimizations or advanced Python features."
                else:
                    message = "For expert-level problems, focus on professional patterns and performance optimization."

            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['sophistication'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'advanced_techniques': result.get('advanced_techniques', []),
                'edge_cases_handled': result.get('edge_cases_handled', []),
                'areas_for_improvement': result.get('areas_for_improvement', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating sophistication with Claude API: {e}")
            feedback['sophistication'] = {
                'score': 0.5,
                'message': 'Could not evaluate sophistication automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _generate_overall_feedback(
        self, grade: int, correctness: float, quality: float, 
        efficiency: float, sophistication: float, is_empty_or_comments_only: bool = False
    ) -> str:
        """Generate overall feedback message based on scores."""
        if grade == 0:
            if is_empty_or_comments_only:
                return "No executable code submitted. Please write actual code to solve the problem."
            else:
                return "Your solution is incorrect. Please review the feedback and try again."
        elif grade >= 9:
            return "Outstanding work! Your solution is correct, well-written, and efficient. Keep it up!"
        elif grade >= 7:
            return "Great job! Your solution works well. Check the feedback for minor improvements."
        elif grade >= 5:
            return "Good effort! Your solution partially works. Review the feedback to improve."
        elif grade >= 3:
            return "Keep trying! Focus on getting the basic solution working first, then optimize."
        else:
            return "Don't give up! Review the problem carefully and try a simpler approach first."
    
    def _has_poor_variable_names(self, code: str) -> bool:
        """Check for poor variable naming conventions."""
        # Look for single letter variables (except common ones like i, j for loops)
        poor_names = re.findall(r'\b[a-z]\b(?!\s*in\s+)', code)
        # Exclude common loop variables and function parameters
        poor_names = [n for n in poor_names if n not in ['i', 'j', 'k', 'n', 'm', 'x', 'y']]
        return len(poor_names) > 3
    
    def _has_duplicate_code(self, code: str) -> bool:
        """Simple check for duplicate code patterns."""
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        # Check for duplicate lines (excluding very short lines)
        meaningful_lines = [line for line in lines if len(line) > 10]
        return len(meaningful_lines) != len(set(meaningful_lines))
    
    def _count_nested_loops(self, tree: ast.AST) -> int:
        """Count maximum nesting depth of loops."""
        max_depth = 0
        
        def count_depth(node, depth=0):
            nonlocal max_depth
            if isinstance(node, (ast.For, ast.While)):
                depth += 1
                max_depth = max(max_depth, depth)
            for child in ast.iter_child_nodes(node):
                count_depth(child, depth)
        
        count_depth(tree)
        return max_depth
    
    def _is_empty_or_comments_only(self, code: str) -> bool:
        """Check if code is empty or contains only comments."""
        if not code or not code.strip():
            return True
        
        # Remove all comments and docstrings
        lines = code.split('\n')
        non_comment_lines = []
        in_multiline_string = False
        multiline_delimiter = None
        
        for line in lines:
            stripped = line.strip()
            
            # Handle multiline strings/docstrings
            if not in_multiline_string:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    multiline_delimiter = '"""' if stripped.startswith('"""') else "'''"
                    if stripped.count(multiline_delimiter) == 1:
                        in_multiline_string = True
                    continue
            else:
                if multiline_delimiter in stripped:
                    in_multiline_string = False
                    multiline_delimiter = None
                continue
            
            # Skip single-line comments
            if stripped.startswith('#'):
                continue
                
            # Skip empty lines
            if not stripped:
                continue
                
            # If we get here, it's a non-comment line
            non_comment_lines.append(line)
        
        # Check if all remaining lines are empty
        remaining_code = '\n'.join(non_comment_lines).strip()
        return len(remaining_code) == 0 
### apps/practice/grading.py END ###

### apps/practice/admin.py BEGIN ###
from django.contrib import admin
from .models import UserProgress, UserQuestionAttempt


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'total_questions_attempted', 'success_rate', 'updated_at']
    list_filter = ['current_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['success_rate', 'created_at', 'updated_at']


@admin.register(UserQuestionAttempt)
class UserQuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'grade', 'attempted_at']
    list_filter = ['grade', 'attempted_at']
    search_fields = ['user__username', 'question__instruction']
    readonly_fields = ['attempted_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'question')

### apps/practice/admin.py END ###

### apps/practice/urls.py BEGIN ###
from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('user-stats/', views.get_user_stats, name='user-stats'),
    path('set-manual-level/', views.set_manual_level, name='set-manual-level'),
    path('next-question/', views.get_next_question, name='next-question'),
    path('run-python/', views.run_python_code, name='run-python'),  # New backend Python execution
    path('submit-solution/', views.submit_solution, name='submit-solution'),
    path('abandon-question/', views.abandon_current_question, name='abandon-question'),
    path('attempt-history/', views.get_attempt_history, name='attempt-history'),
    path('clear-progress/', views.clear_user_progress, name='clear-progress'),
] 
### apps/practice/urls.py END ###

### apps/practice/__init__.py BEGIN ###

### apps/practice/__init__.py END ###

### apps/practice/apps.py BEGIN ###
from django.apps import AppConfig


class PracticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.practice'

### apps/practice/apps.py END ###

### apps/practice/serializers.py BEGIN ###
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt


class UserStatsSerializer(serializers.ModelSerializer):
    """Serializer for user statistics."""
    username = serializers.CharField(source='user.username', read_only=True)
    success_rate = serializers.IntegerField(read_only=True)
    average_grade = serializers.FloatField(read_only=True)
    
    class Meta:
        model = UserProgress
        fields = [
            'username',
            'current_level',
            'manual_level',
            'total_questions_attempted',
            'correct_answers_count',
            'success_rate',
            'average_grade',
            'consecutive_high_grades',
            'consecutive_low_grades'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Python programming questions."""
    
    class Meta:
        model = PythonProgrammingQuestion
        fields = [
            'id',
            'instruction',
            'input',
            'output',
            'difficulty_level'
        ]


class CodeSubmissionSerializer(serializers.Serializer):
    """Serializer for code submission."""
    question_id = serializers.IntegerField()
    code = serializers.CharField(allow_blank=True)  # Allow empty code for grade 0
    
    def validate_question_id(self, value):
        if not PythonProgrammingQuestion.objects.filter(id=value).exists():
            raise serializers.ValidationError("Question not found.")
        return value


class CodeExecutionSerializer(serializers.Serializer):
    """Serializer for code execution (without submission)."""
    code = serializers.CharField(allow_blank=True)  # Allow empty code for testing
    test_input = serializers.CharField(required=False, allow_blank=True)


class ManualLevelSerializer(serializers.Serializer):
    """Serializer for setting manual difficulty level."""
    level = serializers.IntegerField(min_value=1, max_value=5)


class LevelChangeSuggestionSerializer(serializers.Serializer):
    """Serializer for level change suggestions."""
    type = serializers.CharField()  # 'level_up' or 'level_down'
    current_level = serializers.IntegerField()
    suggested_level = serializers.IntegerField()
    reason = serializers.CharField()


class GradeFeedbackSerializer(serializers.Serializer):
    """Serializer for grade and feedback response."""
    grade = serializers.IntegerField(min_value=0, max_value=10)
    feedback = serializers.DictField()
    test_results = serializers.DictField()
    execution_time = serializers.FloatField(required=False)
    level_changed = serializers.BooleanField()
    new_level = serializers.IntegerField(required=False)
    level_suggestion = serializers.DictField(required=False)
    
    
class AttemptHistorySerializer(serializers.ModelSerializer):
    """Serializer for attempt history."""
    question_instruction = serializers.CharField(
        source='question.instruction', 
        read_only=True
    )
    
    class Meta:
        model = UserQuestionAttempt
        fields = [
            'id',
            'question_id',
            'question_instruction',
            'submitted_code',
            'grade',
            'execution_time',
            'test_results',
            'feedback',
            'attempted_at'
        ] 
### apps/practice/serializers.py END ###

### apps/practice/models.py BEGIN ###
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion


class UserProgress(models.Model):
    """
    Tracks user's progress through the coding challenges.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='practice_progress'
    )
    current_level = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Current difficulty level (1-5)"
    )
    manual_level = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User's manually set difficulty level preference (1-5)"
    )
    current_question = models.ForeignKey(
        PythonProgrammingQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_users',
        help_text="The question currently assigned to the user"
    )
    question_assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the current question was assigned"
    )
    consecutive_high_grades = models.IntegerField(
        default=0,
        help_text="Number of consecutive grades 7-10"
    )
    consecutive_low_grades = models.IntegerField(
        default=0,
        help_text="Number of consecutive grades 0-3"
    )
    total_questions_attempted = models.IntegerField(
        default=0,
        help_text="Total number of questions attempted"
    )
    correct_answers_count = models.IntegerField(
        default=0,
        help_text="Number of correct answers (grades 7-10)"
    )
    total_score = models.IntegerField(
        default=0,
        help_text="Sum of all grades received"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['current_level']),
            models.Index(fields=['manual_level']),
            models.Index(fields=['current_question']),
        ]

    def __str__(self):
        return f"{self.user.username} - Level {self.current_level} (Manual: {self.manual_level})"

    @property
    def success_rate(self):
        """Calculate success rate as percentage of correct answers (grades 7-10)."""
        if self.total_questions_attempted == 0:
            return 0
        return round((self.correct_answers_count / self.total_questions_attempted) * 100)

    @property
    def average_grade(self):
        """Calculate average grade as total_score / total_questions_attempted."""
        if self.total_questions_attempted == 0:
            return 0.0
        return round(self.total_score / self.total_questions_attempted, 1)

    def assign_question(self, question):
        """Assign a new question to the user."""
        from django.utils import timezone
        self.current_question = question
        self.question_assigned_at = timezone.now()
        self.save()

    def clear_current_question(self):
        """Clear the current question after submission."""
        self.current_question = None
        self.question_assigned_at = None
        self.save()

    def update_level(self, new_grade):
        """Update user level based on new grade."""
        if new_grade >= 7:
            self.consecutive_high_grades += 1
            self.consecutive_low_grades = 0
            if self.consecutive_high_grades >= 3 and self.current_level < 5:
                self.current_level += 1
                self.consecutive_high_grades = 0
        elif new_grade <= 3:  # This includes grade 0
            self.consecutive_low_grades += 1
            self.consecutive_high_grades = 0
            if self.consecutive_low_grades >= 3 and self.current_level > 1:
                self.current_level -= 1
                self.consecutive_low_grades = 0
        else:
            # Grade 4-6: reset both counters
            self.consecutive_high_grades = 0
            self.consecutive_low_grades = 0
        
        self.save()

    def check_level_change_suggestion(self, new_grade):
        """Check if user should be prompted for level change based on consecutive grades."""
        suggestion = None
        
        if new_grade >= 7:
            new_consecutive_high = self.consecutive_high_grades + 1
            if new_consecutive_high >= 3 and self.manual_level < 5:
                suggestion = {
                    'type': 'level_up',
                    'current_level': self.manual_level,
                    'suggested_level': self.manual_level + 1,
                    'reason': 'You have 3 consecutive high grades (7+)! Consider increasing difficulty.'
                }
        elif new_grade <= 3:
            new_consecutive_low = self.consecutive_low_grades + 1
            if new_consecutive_low >= 3 and self.manual_level > 1:
                suggestion = {
                    'type': 'level_down',
                    'current_level': self.manual_level,
                    'suggested_level': self.manual_level - 1,
                    'reason': 'You have 3 consecutive low grades (3-). Consider decreasing difficulty.'
                }
        
        return suggestion

    def set_manual_level(self, level):
        """Set the user's manual level preference."""
        if 1 <= level <= 5:
            self.manual_level = level
            # Reset consecutive grades counters when user manually sets level
            self.consecutive_high_grades = 0
            self.consecutive_low_grades = 0
            self.save()
            return True
        return False

    def get_effective_level(self):
        """Get the level to use for next question (manual level takes precedence)."""
        return self.manual_level


class UserQuestionAttempt(models.Model):
    """
    Records each attempt a user makes at solving a question.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_attempts'
    )
    question = models.ForeignKey(
        PythonProgrammingQuestion,
        on_delete=models.CASCADE,
        related_name='user_attempts'
    )
    submitted_code = models.TextField(
        help_text="The code submitted by the user"
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Grade received (0-10, where 0 is for empty/comments-only code)"
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Code execution time in seconds"
    )
    test_results = models.JSONField(
        default=dict,
        help_text="Detailed test case results"
    )
    feedback = models.JSONField(
        default=dict,
        help_text="Detailed feedback on the submission"
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Question Attempt'
        verbose_name_plural = 'User Question Attempts'
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['user', 'question']),
            models.Index(fields=['attempted_at']),
            models.Index(fields=['grade']),
        ]

    def __str__(self):
        return f"{self.user.username} - Question {self.question.id} - Grade: {self.grade}"

### apps/practice/models.py END ###

### apps/authentication/tests.py BEGIN ###
from django.test import TestCase

# Create your tests here.

### apps/authentication/tests.py END ###

### apps/authentication/views.py BEGIN ###
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .authentication import JWTOnlyAuthentication
import logging

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user and blacklist their JWT token"""
    logger.info(f"[logout_view] Logging out user: {request.user.username}")
    
    try:
        # Get the refresh token from request body
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            logger.info(f"[logout_view] Blacklisting refresh token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            logger.warning(f"[logout_view] No refresh token provided")
        
        logger.info(f"[logout_view] Logout completed for user: {request.user.username}")
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        logger.error(f"[logout_view] Error during logout: {str(e)}")
        return Response({'error': 'Logout failed'}, status=400)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def user_profile_view(request):
    """Get current user profile"""
    logger.info(f"[user_profile_view] Request user: {request.user.username}")
    
    serializer = UserSerializer(request.user)
    response_data = serializer.data
    
    response = Response(response_data)
    # Add cache control headers to prevent browser caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    try:
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token),
        })
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token_view(request):
    """Verify if an access token is still valid"""
    try:
        token = request.data.get('token')
        if not token:
            return Response(
                {'valid': False, 'error': 'No token provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to decode and validate the token
        try:
            access_token = AccessToken(token)
            # Token is valid
            return Response({
                'valid': True,
                'user_id': access_token['user_id'],
                'exp': access_token['exp'],
                'token_type': access_token['token_type']
            })
        except TokenError as e:
            return Response({
                'valid': False,
                'error': str(e)
            })
            
    except Exception as e:
        return Response(
            {'valid': False, 'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

### apps/authentication/views.py END ###

### apps/authentication/admin.py BEGIN ###
from django.contrib import admin

# Register your models here.

### apps/authentication/admin.py END ###

### apps/authentication/middleware.py BEGIN ###
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPIMiddleware(MiddlewareMixin):
    """
    Middleware to disable CSRF protection for API endpoints.
    API authentication is handled by JWT tokens which are not vulnerable to CSRF.
    """
    def process_request(self, request):
        # Disable CSRF for all /api/ endpoints
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None


class ClearSessionForAPIMiddleware(MiddlewareMixin):
    """
    Middleware to ensure API endpoints use JWT authentication only.
    This prevents session authentication from interfering with JWT auth.
    """
    def process_request(self, request):
        # For API endpoints, clear any session-based user to ensure JWT takes precedence
        if request.path.startswith('/api/'):
            # Save the session key for logging
            session_key = getattr(request.session, 'session_key', None) if hasattr(request, 'session') else None
            
            # Set user to anonymous to force JWT authentication
            request.user = AnonymousUser()
            
            # Log if we're overriding a session user
            if session_key and hasattr(request, 'session') and '_auth_user_id' in request.session:
                import logging
                logger = logging.getLogger(__name__)
                logger.debug(f"[ClearSessionForAPIMiddleware] Cleared session user for API endpoint: {request.path}")
        
        return None 
### apps/authentication/middleware.py END ###

### apps/authentication/urls.py BEGIN ###
from django.urls import path
from .views import (
    RegisterView,
    login_view,
    logout_view,
    user_profile_view,
    refresh_token_view,
    verify_token_view,
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='profile'),
    path('refresh/', refresh_token_view, name='refresh'),
    path('verify/', verify_token_view, name='verify'),
] 
### apps/authentication/urls.py END ###

### apps/authentication/authentication.py BEGIN ###
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class JWTOnlyAuthentication(JWTAuthentication):
    """
    JWT-only authentication for API endpoints.
    Simple and clean - no session fallbacks.
    """
    
    def authenticate(self, request):
        logger.debug(f"[JWTOnlyAuthentication] Authenticating request to {request.path}")
        
        # Get the JWT token from the Authorization header
        header = self.get_header(request)
        if header is None:
            logger.debug(f"[JWTOnlyAuthentication] No Authorization header found")
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.debug(f"[JWTOnlyAuthentication] No valid token in header")
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        
        logger.info(f"[JWTOnlyAuthentication] Authenticated user: {user.username} (ID: {user.id})")
        
        return (user, validated_token) 


class HybridAuthentication(JWTAuthentication):
    """
    Hybrid authentication for django-ai-assistant endpoints.
    Tries JWT first, then session auth for non-API endpoints only.
    """
    
    def authenticate(self, request):
        logger.debug(f"[HybridAuthentication] Authenticating request to {request.path}")
        
        # First try JWT authentication
        try:
            jwt_result = super().authenticate(request)
            if jwt_result:
                user, token = jwt_result
                logger.info(f"[HybridAuthentication] JWT authenticated user: {user.username}")
                return jwt_result
        except AuthenticationFailed:
            logger.debug(f"[HybridAuthentication] JWT auth failed for path: {request.path}")
        except Exception as e:
            logger.error(f"[HybridAuthentication] JWT auth error: {e}")
        
        # Fall back to session auth for non-API endpoints only
        if not request.path.startswith('/api/'):
            try:
                session_auth = SessionAuthentication()
                session_result = session_auth.authenticate(request)
                if session_result:
                    user, auth = session_result
                    logger.info(f"[HybridAuthentication] Session authenticated user: {user.username}")
                    return session_result
            except Exception as e:
                logger.error(f"[HybridAuthentication] Session auth error: {e}")
        
        return None 
### apps/authentication/authentication.py END ###

### apps/authentication/__init__.py BEGIN ###

### apps/authentication/__init__.py END ###

### apps/authentication/permissions.py BEGIN ###
from rest_framework import permissions


class IsAuthenticatedForAIAssistant(permissions.BasePermission):
    """
    Custom permission to allow authenticated users to access AI Assistant endpoints
    """
    def has_permission(self, request, view):
        # Allow OPTIONS requests for CORS
        if request.method == 'OPTIONS':
            return True
        
        # Require authentication for all other requests
        return request.user and request.user.is_authenticated 
### apps/authentication/permissions.py END ###

### apps/authentication/apps.py BEGIN ###
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'

### apps/authentication/apps.py END ###

### apps/authentication/serializers.py BEGIN ###
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) 
### apps/authentication/serializers.py END ###

### apps/authentication/models.py BEGIN ###
from django.db import models

# Create your models here.

### apps/authentication/models.py END ###

### apps/instructions_difficulty_eval/instructions_difficulty_eval.py BEGIN ###
#!/usr/bin/env python3
"""
Instructions Difficulty Evaluation Script

This script evaluates the difficulty of Python programming questions using Claude API
and saves the results to a PostgreSQL database using Django ORM.

Usage:
    python instructions_difficulty_eval.py

Make sure to set the CLAUDE_API_KEY in your env/.env file before running.
"""

CSV_FILE_PATH = "data/Python Programming Questions Dataset.csv"
SAMPLE_SIZE = 500

# CSV_FILE_PATH = "data/sample_questions.csv"
# SAMPLE_SIZE = 5

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_interview_preparation_platform.settings")
django.setup()

from difficulty_evaluator import DifficultyEvaluator

def main():
    """
    Main function to run the difficulty evaluation process.
    """
    print("="*60)
    print("PYTHON PROGRAMMING QUESTIONS DIFFICULTY EVALUATION")
    print("="*60)
    print("This script will:")
    print(f"1. Load {SAMPLE_SIZE} random questions from the CSV dataset")
    print("2. Evaluate each question's difficulty using Claude API")
    print("3. Save results to PostgreSQL database")
    print("="*60)
    
    # Check if Claude API key is set
    if not os.getenv('CLAUDE_API_KEY') or os.getenv('CLAUDE_API_KEY') == 'your_claude_api_key_here':
        print("ERROR: Please set your CLAUDE_API_KEY in the env/.env file")
        print("Current value:", os.getenv('CLAUDE_API_KEY', 'Not set'))
        return
    
    try:
        # Path to the CSV file
        csv_file_path = CSV_FILE_PATH
        
        # Check if CSV file exists
        if not Path(csv_file_path).exists():
            print(f"ERROR: CSV file not found at {csv_file_path}")
            return
        
        print(f"Starting evaluation process...")
        print(f"CSV file: {csv_file_path}")
        print(f"Sample size: {SAMPLE_SIZE} questions")
        print("-" * 60)
        
        # Create evaluator and process questions
        evaluator = DifficultyEvaluator(csv_file_path)
        summary = evaluator.process_questions(sample_size=SAMPLE_SIZE)
        
        # Print results
        print("\n" + "="*50)
        print("DIFFICULTY EVALUATION COMPLETE")
        print("="*50)
        print(f"Total questions processed: {summary['total_processed']}")
        print(f"Successfully evaluated: {summary['successfully_evaluated']}")
        print(f"Failed evaluations: {summary['failed_evaluations']}")
        print(f"Saved to database: {summary['saved_to_database']}")
        
        # Get detailed summary
        detailed_summary = evaluator.get_processing_summary()
        print(f"\nDifficulty distribution:")
        for level, count in detailed_summary['difficulty_distribution'].items():
            print(f"  Level {level}: {count} questions")
        
        if detailed_summary['failed_questions']:
            print(f"\nFailed questions (first 5):")
            for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                print(f"  {i}. Error: {failed['error']}")
                print(f"     Question ID: {failed['question']['question_id']}")
                print(f"     Instruction: {failed['question']['instruction'][:100]}...")
        
        print("\n" + "="*50)
        print("Process completed successfully!")
        print("Check your PostgreSQL database for the results.")
        print("="*50)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

### apps/instructions_difficulty_eval/instructions_difficulty_eval.py END ###

### apps/instructions_difficulty_eval/difficulty_service.py BEGIN ###
import logging
from typing import Tuple, Optional
from langchain.prompts import PromptTemplate
from apps.api import ClaudeService

logger = logging.getLogger(__name__)


class DifficultyEvaluationService:
    """
    Service for evaluating Python programming question difficulty using Claude API.
    """
    
    def __init__(self):
        """Initialize the service with Claude API client."""
        self.claude_service = ClaudeService()
    
    def evaluate_instruction_difficulty(
        self, 
        instruction: str, 
        input: str, 
        output: str
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Evaluate the explanation and difficulty level of a programming instruction.
        
        Args:
            instruction: The programming instruction to evaluate
            input: Input example for the question
            output: Expected output for the question
            
        Returns:
            tuple[str, int]: Explanation text and numeric difficulty level (1-5), 
                           or (None, None) if evaluation fails
        """
        try:
            prompt = self._create_difficulty_evaluation_prompt(instruction, input, output)
            
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=20000,
                temperature=0.1
            )
            
            # Parse the response
            explanation_text, difficulty_level = self._parse_difficulty_response(response_text)
            return explanation_text, difficulty_level
            
        except Exception as e:
            logger.error(f"Error evaluating instruction difficulty: {e}")
            logger.error(f"Instruction: {instruction[:100]}...")
            return None, None
    
    def _create_difficulty_evaluation_prompt(self, instruction: str, input: str, output: str) -> str:
        """
        Create a prompt for Claude to evaluate instruction difficulty.
        
        Args:
            instruction: The programming instruction
            input: Input example
            output: Expected output
            
        Returns:
            str: Formatted prompt for Claude API
        """
        prompt_template = PromptTemplate(
            input_variables=["instruction", "input", "output"],
            template="""Please help me with the task of ranking the difficulty level of a Python programming question (instruction),   
                given the input and output.

                The instruction, input and output are given at the end of this prompt.

                The instruction should be assigned a numeric difficulty level (1, 2, 3, 4, or 5). (1 - easiest, 5 - hardest). 

                Here are the difficulty level definitions:
                **1 = Very Easy (Beginner - Basic Python Syntax)**
                - Simple arithmetic operations and basic calculations
                - Basic print statements and variable assignments
                - Simple list/string operations without complex logic
                - Basic loops and conditionals with straightforward logic
                - Examples: "Calculate sum of two numbers", "Print numbers 1-10", "Check if number is even"

                **2 = Easy (Fundamental Programming Concepts)**
                - Basic function definitions with simple parameters
                - Elementary list/dictionary manipulation
                - Simple string processing and formatting
                - Basic file operations
                - Straightforward control flow with multiple conditions
                - Examples: "Remove duplicates from list", "Count occurrences in string", "Basic calculator functions"

                **3 = Medium (Intermediate Python Features)**
                - List comprehensions and lambda functions
                - Basic sorting and searching algorithms
                - Simple recursion (Fibonacci, factorial)
                - Basic object-oriented programming (simple classes)
                - Exception handling
                - Working with modules and imports
                - Examples: "Binary search implementation", "Simple class definitions", "Recursive functions"

                **4 = Hard (Advanced Programming Concepts)**
                - Complex data structures (linked lists, trees, stacks)
                - Advanced algorithms (DFS, BFS, dynamic programming)
                - Web scraping and API interactions
                - Database connections and operations
                - Advanced OOP concepts (inheritance, polymorphism)
                - Regular expressions and pattern matching
                - Examples: "Binary tree traversal", "Web scraping with BeautifulSoup", "REST API development"

                **5 = Very Hard (Expert Level - Professional Development)**
                - Machine learning model implementation
                - Asynchronous programming and concurrency
                - Advanced data analysis with NumPy/Pandas
                - Cloud services integration (AWS Lambda)
                - Complex system design and architecture
                - Performance optimization and algorithm complexity
                - Advanced web development frameworks
                - Examples: "ML classifier with scikit-learn", "AWS Lambda functions", "Asynchronous web scraping"

                Please respond with:
                (1) All the text explaning how you decided upon the difficulty level.
                (2) The last character at the very end should be the difficulty level numeric value (1, 2, 3, 4, or 5) alone, 
                without '**' or any other text. 

                Instruction: "{instruction}"
                Input: "{input}"
                Output: "{output}"
                """
        )
        return prompt_template.format(
            instruction=instruction,
            input=input,
            output=output
        )
    
    def _parse_difficulty_response(self, response_text: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse the explanation and difficulty level from Claude's response.
        
        Args:
            response_text: Claude's response text
            
        Returns:
            tuple[str, int]: Parsed explanation text and numeric difficulty level,
                           or (None, None) if parsing fails
        """
        try:
            difficulty_str = response_text.strip()

            # Extract explanation text from response
            explanation_text = difficulty_str[0:-1]

            # Extract numeric value from response
            numeric_difficulty_str = difficulty_str[-1]
            if numeric_difficulty_str.isdigit():
                numeric_difficulty = int(numeric_difficulty_str)
                if 1 <= numeric_difficulty <= 5:
                    return explanation_text, numeric_difficulty
                        
            logger.warning(f"Could not parse difficulty from response: {response_text}")
            return None, None
            
        except Exception as e:
            logger.error(f"Error parsing difficulty response: {e}")
            return None, None 
### apps/instructions_difficulty_eval/difficulty_service.py END ###

### apps/instructions_difficulty_eval/__init__.py BEGIN ###
# Instructions Difficulty Evaluation App 

from .difficulty_service import DifficultyEvaluationService

__all__ = ['DifficultyEvaluationService'] 
### apps/instructions_difficulty_eval/__init__.py END ###

### apps/instructions_difficulty_eval/difficulty_evaluator.py BEGIN ###
import os
import sys
import django
import logging
from typing import List, Dict, Any
from pathlib import Path
from tqdm import tqdm

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from apps.instructions_difficulty_eval.difficulty_service import DifficultyEvaluationService
from apps.instructions_difficulty_eval.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class DifficultyEvaluator:
    """
    Main class that orchestrates the difficulty evaluation process.
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the difficulty evaluator.
        
        Args:
            csv_file_path (str): Path to the CSV file containing questions
        """
        self.csv_file_path = csv_file_path
        self.data_processor = DataProcessor(csv_file_path)
        self.difficulty_service = DifficultyEvaluationService()
        self.processed_questions = []
        self.failed_questions = []
        self.saved_count = 0
    
    def process_questions(self, sample_size: int = 500) -> Dict[str, int]:
        """
        Process questions by evaluating difficulty and saving to database.
        
        Args:
            sample_size (int): Number of questions to sample and process
            
        Returns:
            Dict[str, int]: Summary of processing results
        """
        try:
            logger.info(f"Starting difficulty evaluation for {sample_size} questions")
            
            # Load and sample data
            self.data_processor.sample_questions(n=sample_size)
            questions_list = self.data_processor.get_questions_list()
            
            logger.info(f"Processing {len(questions_list)} questions")
            
            # Process each question
            for i, question in enumerate(tqdm(questions_list, desc="Processing questions"), 1):
                try:
                    self._process_single_question(question, i, len(questions_list))
                except Exception as e:
                    logger.error(f"Error processing question {i}: {e}")
                    self.failed_questions.append({
                        'question': question,
                        'error': str(e)
                    })
            
            # Return summary
            summary = {
                'total_processed': len(questions_list),
                'successfully_evaluated': len(self.processed_questions),
                'failed_evaluations': len(self.failed_questions),
                'saved_to_database': self.saved_count
            }
            
            logger.info(f"Processing complete: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Error in process_questions: {e}")
            raise
    
    def _process_single_question(self, question: Dict[str, Any], current: int, total: int) -> None:
        """
        Process a single question by evaluating its difficulty and saving to database.
        
        Args:
            question (Dict[str, Any]): Question data
            current (int): Current question number
            total (int): Total number of questions
        """
        try:
            # Validate question data
            if not self.data_processor.validate_question_data(question):
                logger.warning(f"Question {current} failed validation, skipping")
                return
            
            instruction = question['instruction']
            logger.info(f"Processing question {current}/{total}: {instruction[:50]}...")

            input = question['input']
            output = question['output']
            
            # Evaluate explanation and numeric difficulty level using Claude API
            explanation_text, difficulty_level = self.difficulty_service.evaluate_instruction_difficulty(instruction, input, output)
            
            question['question_id'] = current
            if difficulty_level is not None:
                # Add explanation and difficulty level to question data
                question['difficulty_explanation'] = explanation_text
                question['difficulty_level'] = difficulty_level

                self.processed_questions.append(question)

                logger.info(f"Question {current} evaluated with difficulty level: {difficulty_level}")

                is_saved = self._save_to_database(question)
                if not is_saved:
                    logger.error(f"Failed to save question {current} to database")
                    self.failed_questions.append({
                        'question': question,
                        'error': 'Failed to save question to database'
                    })
            else:
                logger.warning(f"Failed to evaluate difficulty for question {current}")
                self.failed_questions.append({
                    'question': question,
                    'error': 'Failed to get difficulty level from Claude API'
                })
                
        except Exception as e:
            logger.error(f"Error processing single question {current}: {e}")
            raise
    
    def _save_to_database(self, question: Dict[str, Any]) -> bool:
        """
        Save processed question to the database and update the saved_count.
        
        Args:
            question (Dict[str, Any]): Question data

        Returns:
            bool: True if question was saved to database, False otherwise
        """
        try:
            logger.info(f"Saving question to database")
            
            # Create and save the model instance
            python_question = PythonProgrammingQuestion(
                instruction=question['instruction'],
                input=question['input'],
                output=question['output'],
                difficulty_explanation=question['difficulty_explanation'],
                difficulty_level=question['difficulty_level']
            )
            python_question.save()
            self.saved_count += 1
            return True
            
        except Exception as e:
            logger.error(f"Error saving question to database: {e}")
            logger.error(f"Question data: {question}")
            return False
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a detailed summary of the processing results.
        
        Returns:
            Dict[str, Any]: Detailed processing summary
        """
        return {
            'processed_questions_count': len(self.processed_questions),
            'failed_questions_count': len(self.failed_questions),
            'failed_questions': self.failed_questions,
            'difficulty_distribution': self._get_difficulty_distribution()
        }
    
    def _get_difficulty_distribution(self) -> Dict[int, int]:
        """
        Get the distribution of difficulty levels in processed questions.
        
        Returns:
            Dict[int, int]: Distribution of difficulty levels
        """
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for question in self.processed_questions:
            difficulty = question.get('difficulty_level')
            if difficulty in distribution:
                distribution[difficulty] += 1
        
        return distribution


def main():
    """
    Main function to run the difficulty evaluation process.
    """
    # Django logging configuration is already set up via settings.py
    # No need for additional basicConfig as it would override Django's logging
    
    try:
        # Path to the CSV file
        csv_file_path = "data/Python Programming Questions Dataset.csv"
        
        # Create evaluator and process questions
        evaluator = DifficultyEvaluator(csv_file_path)
        summary = evaluator.process_questions(sample_size=500)
        
        # Print results
        print("\n" + "="*50)
        print("DIFFICULTY EVALUATION COMPLETE")
        print("="*50)
        print(f"Total questions processed: {summary['total_processed']}")
        print(f"Successfully evaluated: {summary['successfully_evaluated']}")
        print(f"Failed evaluations: {summary['failed_evaluations']}")
        print(f"Saved to database: {summary['saved_to_database']}")
        
        # Get detailed summary
        detailed_summary = evaluator.get_processing_summary()
        print(f"\nDifficulty distribution:")
        for level, count in detailed_summary['difficulty_distribution'].items():
            print(f"  Level {level}: {count} questions")
        
        if detailed_summary['failed_questions']:
            print(f"\nFailed questions:")
            for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                print(f"  {i}. Error: {failed['error']}")
                print(f"     Instruction: {failed['question']['instruction'][:100]}...")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 
### apps/instructions_difficulty_eval/difficulty_evaluator.py END ###

### apps/instructions_difficulty_eval/apps.py BEGIN ###
from django.apps import AppConfig


class InstructionsDifficultyEvalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.instructions_difficulty_eval' 
### apps/instructions_difficulty_eval/apps.py END ###

### apps/instructions_difficulty_eval/data_processor.py BEGIN ###
import pandas as pd
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Class for processing the Python programming questions dataset.
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the data processor with CSV file path.
        
        Args:
            csv_file_path (str): Path to the CSV file containing questions
        """
        self.csv_file_path = Path(csv_file_path)
        self.data = None
        self.sample_data = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            Exception: If there's an error loading the data
        """
        try:
            if not self.csv_file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
            
            self.data = pd.read_csv(self.csv_file_path)
            logger.info(f"Loaded {len(self.data)} questions from {self.csv_file_path}")
            logger.info(f"Data shape: {self.data.shape}")
            logger.info(f"Columns: {list(self.data.columns)}")
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data from {self.csv_file_path}: {e}")
            raise
    
    def sample_questions(self, n: int = 500, random_state: int = 42) -> pd.DataFrame:
        """
        Sample n questions from the dataset.
        
        Args:
            n (int): Number of questions to sample
            random_state (int): Random state for reproducibility
            
        Returns:
            pd.DataFrame: Sampled questions
        """
        try:
            if self.data is None:
                self.load_data()
            
            # Ensure we don't sample more than available data
            sample_size = min(n, len(self.data))
            
            self.sample_data = self.data.sample(n=sample_size, random_state=random_state)
            logger.info(f"Sampled {len(self.sample_data)} questions")
            
            return self.sample_data
            
        except Exception as e:
            logger.error(f"Error sampling questions: {e}")
            raise
    
    def get_questions_list(self) -> List[Dict[str, Any]]:
        """
        Convert sampled questions to a list of dictionaries.
        
        Returns:
            List[Dict[str, Any]]: List of question dictionaries
        """
        try:
            if self.sample_data is None:
                raise ValueError("No sampled data available. Call sample_questions() first.")
            
            questions_list = []
            for _, row in self.sample_data.iterrows():
                question_dict = {
                    'instruction': str(row.get('Instruction', '')).strip(),
                    'input': str(row.get('Input', '')).strip() if pd.notna(row.get('Input')) else '',
                    'output': str(row.get('Output', '')).strip() if pd.notna(row.get('Output')) else ''
                }
                questions_list.append(question_dict)
            
            logger.info(f"Converted {len(questions_list)} questions to dictionary format")
            return questions_list
            
        except Exception as e:
            logger.error(f"Error converting questions to list: {e}")
            raise
    
    def validate_question_data(self, question: Dict[str, Any]) -> bool:
        """
        Validate that a question has the required fields.
        
        Args:
            question (Dict[str, Any]): Question dictionary
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['instruction', 'input', 'output']
        
        for field in required_fields:
            if field not in question:
                logger.warning(f"Missing field '{field}' in question")
                return False
        
        # Check if instruction is not empty
        if not question['instruction'] or question['instruction'].strip() == '':
            logger.warning("Empty instruction found")
            return False
        
        return True 
### apps/instructions_difficulty_eval/data_processor.py END ###

### apps/instructions_difficulty_eval/models.py BEGIN ###
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PythonProgrammingQuestion(models.Model):
    """
    Model to store Python programming questions with their difficulty levels.
    """
    instruction = models.TextField(
        help_text="The programming instruction or question"
    )
    input = models.TextField(
        blank=True,
        help_text="Input example or parameters for the question"
    )
    output = models.TextField(
        help_text="Expected output or solution for the question"
    )
    difficulty_explanation = models.TextField(
        blank=True,
        help_text="Explanation of the difficulty level"
    )
    difficulty_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Difficulty level from 1 (easiest) to 5 (hardest)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'python_programming_questions'
        verbose_name = 'Python Programming Question'
        verbose_name_plural = 'Python Programming Questions'
        indexes = [
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Question (Difficulty: {self.difficulty_level}): {self.instruction[:50]}..." 
### apps/instructions_difficulty_eval/models.py END ###

### apps/instructions_difficulty_eval/management/__init__.py BEGIN ###
# Management package for instructions_difficulty_eval app 
### apps/instructions_difficulty_eval/management/__init__.py END ###

### apps/instructions_difficulty_eval/management/commands/evaluate_difficulty.py BEGIN ###
from django.core.management.base import BaseCommand, CommandError
from apps.instructions_difficulty_eval.difficulty_evaluator import DifficultyEvaluator
import logging


class Command(BaseCommand):
    help = 'Evaluate difficulty of Python programming questions using Claude API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sample-size',
            type=int,
            default=500,
            help='Number of questions to sample and evaluate (default: 500)'
        )
        parser.add_argument(
            '--csv-path',
            type=str,
            default='data/Python Programming Questions Dataset.csv',
            help='Path to the CSV file containing questions'
        )

    def handle(self, *args, **options):
        # Django logging configuration is already set up via settings.py
        # No need for additional basicConfig as it would override Django's logging

        sample_size = options['sample_size']
        csv_path = options['csv_path']

        self.stdout.write(
            self.style.SUCCESS(f'Starting difficulty evaluation for {sample_size} questions...')
        )

        try:
            # Create evaluator and process questions
            evaluator = DifficultyEvaluator(csv_path)
            summary = evaluator.process_questions(sample_size=sample_size)

            # Print results
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('DIFFICULTY EVALUATION COMPLETE'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(f'Total questions processed: {summary["total_processed"]}')
            self.stdout.write(f'Successfully evaluated: {summary["successfully_evaluated"]}')
            self.stdout.write(f'Failed evaluations: {summary["failed_evaluations"]}')
            self.stdout.write(f'Saved to database: {summary["saved_to_database"]}')

            # Get detailed summary
            detailed_summary = evaluator.get_processing_summary()
            self.stdout.write('\nDifficulty distribution:')
            for level, count in detailed_summary['difficulty_distribution'].items():
                self.stdout.write(f'  Level {level}: {count} questions')

            if detailed_summary['failed_questions']:
                self.stdout.write(self.style.WARNING('\nFailed questions (first 5):'))
                for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                    self.stdout.write(f'  {i}. Error: {failed["error"]}')
                    self.stdout.write(f'     Instruction: {failed["question"]["instruction"][:100]}...')

            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully completed evaluation!')
            )

        except Exception as e:
            raise CommandError(f'Error during evaluation: {e}') 
### apps/instructions_difficulty_eval/management/commands/evaluate_difficulty.py END ###

### apps/instructions_difficulty_eval/management/commands/__init__.py BEGIN ###
# Commands package for instructions_difficulty_eval app 
### apps/instructions_difficulty_eval/management/commands/__init__.py END ###

### apps/rag/ai_assistants.py BEGIN ###
from langchain_community.retrievers import TFIDFRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

from django_ai_assistant import AIAssistant
from apps.rag.models import DjangoDocPage


class DjangoDocsAssistant(AIAssistant):
    id = "django_docs_assistant"  # noqa: A003
    name = "Django Docs Assistant"
    instructions = (
        "You are an assistant for answering questions related to Django web framework. "
        "Use the following pieces of retrieved context from Django's documentation to answer "
        "the user's question. If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise."
    )
    model = "gpt-4o-mini"
    has_rag = True

    def get_retriever(self) -> BaseRetriever:
        # NOTE: on a production application, you should persist or cache the retriever,
        # updating it only when documents change.
        docs = (page.as_langchain_document() for page in DjangoDocPage.objects.all())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        return TFIDFRetriever.from_documents(splits)

### apps/rag/ai_assistants.py END ###

### apps/rag/admin.py BEGIN ###
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.rag.models import DjangoDocPage


@admin.register(DjangoDocPage)
class DjangoDocPageAdmin(admin.ModelAdmin):
    list_display = ("path", "django_docs_url")
    search_fields = ("path",)

    @admin.display(ordering="path", description="Django Docs URL")
    def django_docs_url(self, obj):
        return mark_safe(f'<a href="{obj.django_docs_url}">{obj.django_docs_url}</a>')  # noqa: S308

### apps/rag/admin.py END ###

### apps/rag/__init__.py BEGIN ###

### apps/rag/__init__.py END ###

### apps/rag/apps.py BEGIN ###
from django.apps import AppConfig


class RAGConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.rag"

### apps/rag/apps.py END ###

### apps/rag/models.py BEGIN ###
from django.db import models

from langchain_core.documents import Document


class DjangoDocPage(models.Model):
    id: int  # noqa: A003
    path = models.CharField(max_length=255, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.path

    def __repr__(self) -> str:
        return f"<DjangoDocPage {self.path}>"

    @property
    def django_docs_url(self):
        # Drop docs/ prefix:
        path = self.path[len("docs/") :]

        if path.endswith("index.txt"):
            # Remove index.txt suffix:
            path = path[: -len("index.txt")]
        else:
            # Remove .txt suffix:
            path = path[: -len(".txt")] + "/"

        return f"https://docs.djangoproject.com/en/stable/{path}"

    def as_langchain_document(self):
        return Document(page_content=self.content, metatags={"id": self.id, "path": self.path})

### apps/rag/models.py END ###

### apps/rag/management/__init__.py BEGIN ###

### apps/rag/management/__init__.py END ###

### apps/rag/management/commands/fetch_django_docs.py BEGIN ###
import tempfile
from typing import Any, cast

from django.conf import settings
from django.core.management.base import BaseCommand

from git import Repo

from apps.rag.models import DjangoDocPage


class Command(BaseCommand):
    help = "Fill the database with Django docs"  # noqa: A003
    django_repo_url = "https://github.com/django/django.git"

    def handle(self, *args, **options):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.stdout.write(self.style.NOTICE("Cloning Django repo to a temporary directory..."))
            repo = Repo.clone_from(self.django_repo_url, temp_dir)
            repo.git.checkout(settings.DJANGO_DOCS_BRANCH)
            self.stdout.write(self.style.NOTICE("Saving docs..."))
            head = repo.heads[settings.DJANGO_DOCS_BRANCH].checkout()
            tree = head.commit.tree
            tree = cast(Any, tree)
            for blob in tree["docs"].traverse(visit_once=True):
                if blob.path.startswith("docs/_ext/"):
                    continue
                if blob.path.startswith("docs/_theme/"):
                    continue
                if blob.path.startswith("docs/man/"):
                    continue
                if blob.path.startswith("docs/README.rst"):
                    continue
                if blob.path.startswith("docs/requirements.txt"):
                    continue

                if blob.path.endswith(".txt"):
                    DjangoDocPage.objects.update_or_create(
                        path=blob.path,
                        defaults={"content": blob.data_stream.read().decode("utf-8")},
                    )

        self.stdout.write(self.style.SUCCESS("Success in saving Django docs to DB"))

### apps/rag/management/commands/fetch_django_docs.py END ###

### apps/rag/management/commands/__init__.py BEGIN ###

### apps/rag/management/commands/__init__.py END ###

### apps/api/tests.py BEGIN ###
from django.test import TestCase

# Create your tests here.

### apps/api/tests.py END ###

### apps/api/views.py BEGIN ###
from django.shortcuts import render

# Create your views here.

### apps/api/views.py END ###

### apps/api/admin.py BEGIN ###
from django.contrib import admin

# Register your models here.

### apps/api/admin.py END ###

### apps/api/__init__.py BEGIN ###
from .claude_service import ClaudeService

__all__ = ['ClaudeService']

### apps/api/__init__.py END ###

### apps/api/claude_service.py BEGIN ###
import os
import logging
from typing import Dict, List, Any
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeService:
    """
    Generic service class for interacting with Claude API.
    This can be used across different Django apps for various AI tasks.
    """
    
    def __init__(self):
        """
        Initialize Claude API client.
        """
        self.api_key = os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
        
        self.client = Anthropic(api_key=self.api_key)
        # Using Claude 4 Sonnet, which is the latest available model
        self.model = "claude-sonnet-4-20250514"
    
    def send_message(
        self, 
        prompt: str, 
        max_tokens: int = 21333,
        temperature: float = 0.1,
        system_message: str = None,
        thinking_mode: bool = True
    ) -> str:
        """
        Send a message to Claude and get a response.
        
        Args:
            prompt: The user prompt to send
            max_tokens: Maximum tokens in response (includes both thinking + answer when thinking_mode=True)
                       Default: 21,333 (maximum without streaming requirement)
                       Automatically increased to minimum 1124 when thinking_mode=True
            temperature: Temperature for response generation (0-1) - ignored when thinking_mode=True (uses 1.0)
            system_message: Optional system message
            thinking_mode: If True, use Claude Advanced Thinking Mode with budget tokens
            
        Returns:
            str: Claude's response text
        """
        try:
            messages = []
            
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            # Add thinking mode parameters if enabled
            if thinking_mode:
                # Ensure max_tokens is sufficient for thinking mode (minimum 1024 + buffer)
                min_required_tokens = 1024 + 100  # 1024 minimum budget + 100 buffer
                if max_tokens < min_required_tokens:
                    max_tokens = min_required_tokens
                    api_params["max_tokens"] = max_tokens
                
                # Use maximum budget tokens (Claude 4 summarizes thinking output)
                # Only need small buffer since thinking is summarized, not full output
                budget_tokens = max_tokens - 100  # Minimal buffer as thinking is summarized
                budget_tokens = max(budget_tokens, 1024)  # Ensure minimum 1024 as required
                
                api_params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": budget_tokens
                }
                # Temperature must be 1 when thinking is enabled (per API docs)
                api_params["temperature"] = 1.0
            else:
                # Only set temperature when thinking is disabled
                api_params["temperature"] = temperature
            
            response = self.client.messages.create(**api_params)
            
            # Find the text content block (thinking blocks come first, then text blocks)
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            
            # Fallback if no text block found
            return ""
            
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise
    
    def send_structured_message(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 21333,
        temperature: float = 0.1,
        thinking_mode: bool = True
    ) -> str:
        """
        Send structured messages to Claude.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens in response (includes both thinking + answer when thinking_mode=True)
                       Default: 21,333 (maximum without streaming requirement)
                       Automatically increased to minimum 1124 when thinking_mode=True
            temperature: Temperature for response generation (0-1) - ignored when thinking_mode=True (uses 1.0)
            thinking_mode: If True, use Claude Advanced Thinking Mode with budget tokens
            
        Returns:
            str: Claude's response text
        """
        try:
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            # Add thinking mode parameters if enabled
            if thinking_mode:
                # Ensure max_tokens is sufficient for thinking mode (minimum 1024 + buffer)
                min_required_tokens = 1024 + 100  # 1024 minimum budget + 100 buffer
                if max_tokens < min_required_tokens:
                    max_tokens = min_required_tokens
                    api_params["max_tokens"] = max_tokens
                
                # Use maximum budget tokens (Claude 4 summarizes thinking output)
                # Only need small buffer since thinking is summarized, not full output
                budget_tokens = max_tokens - 100  # Minimal buffer as thinking is summarized
                budget_tokens = max(budget_tokens, 1024)  # Ensure minimum 1024 as required
                
                api_params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": budget_tokens
                }
                # Temperature must be 1 when thinking is enabled (per API docs)
                api_params["temperature"] = 1.0
            else:
                # Only set temperature when thinking is disabled
                api_params["temperature"] = temperature
            
            response = self.client.messages.create(**api_params)
            
            # Find the text content block (thinking blocks come first, then text blocks)
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            
            # Fallback if no text block found
            return ""
            
        except Exception as e:
            logger.error(f"Error calling Claude API with structured messages: {e}")
            raise 
### apps/api/claude_service.py END ###

### apps/api/apps.py BEGIN ###
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'

### apps/api/apps.py END ###

### apps/api/models.py BEGIN ###
from django.db import models

# Create your models here.

### apps/api/models.py END ###

### apps/demo/views.py BEGIN ###
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login

from pydantic import ValidationError

from django_ai_assistant.api.schemas import (
    ThreadIn,
    ThreadMessageIn,
)
from django_ai_assistant.helpers.use_cases import (
    create_message,
    create_thread,
    get_thread_messages,
    get_threads,
)
from django_ai_assistant.models import Thread

from apps.rag.ai_assistants import DjangoDocsAssistant


class HybridAuthMixin:
    """
    Mixin that allows both session and JWT authentication for views.
    This is useful for HTMX views that can be accessed from both
    Django templates (session auth) and React app (JWT auth).
    """
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated via session
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        # Try JWT authentication
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                request.user = auth_result[0]
                request.auth = auth_result[1]
                return super().dispatch(request, *args, **kwargs)
        except Exception:
            pass
        
        # If neither authentication method works, redirect to login
        return redirect(f'/login?next={request.path}')


def react_index(request, **kwargs):
    return render(request, "demo/react_index.html")


class BaseAIAssistantView(HybridAuthMixin, TemplateView):
    def get_assistant_id(self, **kwargs):
        """Returns the DjangoDocsAssistant. Replace this with your own logic."""
        return DjangoDocsAssistant.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        threads = list(get_threads(user=self.request.user))
        context.update(
            {
                "assistant_id": self.get_assistant_id(**kwargs),
                "threads": threads,
            }
        )
        return context


class AIAssistantChatHomeView(BaseAIAssistantView):
    template_name = "demo/chat_home.html"

    # POST to create thread:
    def post(self, request, *args, **kwargs):
        try:
            thread_data = ThreadIn(**request.POST)
        except ValidationError:
            messages.error(request, "Invalid thread data")
            return redirect("chat_home")

        thread = create_thread(
            name=thread_data.name,
            user=request.user,
            request=request,
        )
        return redirect("chat_thread", thread_id=thread.id)


class AIAssistantChatThreadView(BaseAIAssistantView):
    template_name = "demo/chat_thread.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread_id = self.kwargs["thread_id"]
        thread = get_object_or_404(Thread, id=thread_id)

        thread_messages = get_thread_messages(
            thread=thread,
            user=self.request.user,
            request=self.request,
        )
        context.update(
            {
                "thread_id": self.kwargs["thread_id"],
                "thread_messages": thread_messages,
            }
        )
        return context

    # POST to create message:
    def post(self, request, *args, **kwargs):
        assistant_id = self.get_assistant_id()
        thread_id = self.kwargs["thread_id"]
        thread = get_object_or_404(Thread, id=thread_id)

        try:
            message = ThreadMessageIn(
                assistant_id=assistant_id,
                content=request.POST.get("content") or None,
            )
        except ValidationError:
            messages.error(request, "Invalid message data")
            return redirect("chat_thread", thread_id=thread_id)

        create_message(
            assistant_id=assistant_id,
            thread=thread,
            user=request.user,
            content=message.content,
            request=request,
        )
        return redirect("chat_thread", thread_id=thread_id)

@api_view(['GET'])
def debug_auth(request):
    """Debug endpoint to check authentication status"""
    return Response({
        'user': str(request.user),
        'is_authenticated': request.user.is_authenticated,
        'auth_header': request.META.get('HTTP_AUTHORIZATION', 'None'),
        'session_key': request.session.session_key if hasattr(request, 'session') else 'No session',
        'has_jwt_auth': hasattr(request, 'auth') and request.auth is not None,
        'path': request.path,
    })

@api_view(['POST'])
def create_session_from_jwt(request):
    """
    Create a Django session from JWT token.
    This allows React app users to access HTMX views that require session auth.
    """
    jwt_auth = JWTAuthentication()
    try:
        auth_result = jwt_auth.authenticate(request)
        if auth_result:
            user, token = auth_result
            # Create a session for the user
            login(request, user)
            return Response({
                'success': True,
                'message': 'Session created successfully',
                'redirect_url': '/htmx/'
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid or missing JWT token'
            }, status=401)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Authentication failed: {str(e)}'
        }, status=401)
### apps/demo/views.py END ###

### apps/demo/middleware.py BEGIN ###
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.models import AnonymousUser


class DjangoAIAssistantAuthMiddleware(MiddlewareMixin):
    """
    Middleware to handle authentication for django-ai-assistant endpoints
    """
    def process_request(self, request):
        # Skip authentication for logout endpoint
        if request.path == '/api/auth/logout/':
            print(f"[DjangoAIAssistantAuthMiddleware] Skipping auth for logout endpoint")
            return
            
        # Only process AI assistant endpoints
        if request.path.startswith('/ai-assistant/'):
            # Try JWT authentication first
            jwt_auth = JWTAuthentication()
            try:
                auth_result = jwt_auth.authenticate(request)
                if auth_result:
                    request.user = auth_result[0]
                    request.auth = auth_result[1]
                    print(f"[DjangoAIAssistantAuthMiddleware] JWT auth successful for user: {request.user}")
                    return
            except Exception as e:
                print(f"[DjangoAIAssistantAuthMiddleware] JWT auth failed: {e}")
            
            # Fall back to session authentication
            session_auth = SessionAuthentication()
            try:
                auth_result = session_auth.authenticate(request)
                if auth_result:
                    request.user = auth_result[0]
                    request.auth = auth_result[1]
                    print(f"[DjangoAIAssistantAuthMiddleware] Session auth successful for user: {request.user}")
                    return
            except Exception as e:
                print(f"[DjangoAIAssistantAuthMiddleware] Session auth failed: {e}")
            
            print(f"[DjangoAIAssistantAuthMiddleware] No authentication found for {request.path}")
            if not hasattr(request, 'user') or isinstance(request.user, AnonymousUser):
                print(f"[DjangoAIAssistantAuthMiddleware] User is anonymous") 
### apps/demo/middleware.py END ###

### apps/demo/urls.py BEGIN ###
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from apps.demo import views


# Import django-ai-assistant views to wrap them
def get_ai_assistant_urls():
    """
    Get django-ai-assistant URLs and ensure they work with our authentication
    """
    from django_ai_assistant.urls import urlpatterns as ai_patterns
    
    # The django-ai-assistant might be using viewsets or API views
    # Let's ensure CSRF is handled properly for API calls
    wrapped_patterns = []
    for pattern in ai_patterns:
        # Keep the original pattern but the views should use our auth
        wrapped_patterns.append(pattern)
    
    return wrapped_patterns


urlpatterns = [
    # Debug endpoint
    path("debug-auth/", views.debug_auth, name="debug_auth"),
    # Session creation endpoint for JWT users
    path("create-session/", views.create_session_from_jwt, name="create_session_from_jwt"),
    # Use the wrapped AI assistant URLs
    path("ai-assistant/", include(get_ai_assistant_urls())),
    path("htmx/", views.AIAssistantChatHomeView.as_view(), name="chat_home"),
    path(
        "htmx/thread/<int:thread_id>/",
        views.AIAssistantChatThreadView.as_view(),
        name="chat_thread",
    ),
    # Catch all for react app:
    path("", views.react_index, {"resource": ""}),
    path("<path:resource>", views.react_index),
]

### apps/demo/urls.py END ###

### apps/demo/__init__.py BEGIN ###

### apps/demo/__init__.py END ###

### apps/demo/apps.py BEGIN ###
from django.apps import AppConfig


class DemoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.demo"

### apps/demo/apps.py END ###

### apps/demo/templatetags/__init__.py BEGIN ###

### apps/demo/templatetags/__init__.py END ###

### apps/demo/templatetags/markdown.py BEGIN ###
from django import template
from django.utils.safestring import mark_safe

from pycmarkgfm import markdown_to_html


register = template.Library()


@register.filter(name="markdown")
def markdown_filter(value):
    if value is None:
        return ""
    return mark_safe(markdown_to_html(value))  # noqa: S308

### apps/demo/templatetags/markdown.py END ###

### apps/demo/templates/base.html BEGIN ###
{% load render_bundle from webpack_loader %}

<!doctype html>
<html lang="en">
  <head>
    <meta charSet="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    />
    {% block title %}
    <title>Interview Preparation Platform</title>
    {% endblock %}

    {% render_bundle 'main' 'css' %}
  </head>
  <body>
    {% csrf_token %}
    {% block content %}{% endblock %}
  </body>
</html>

### apps/demo/templates/base.html END ###

### apps/demo/templates/demo/chat_thread.html BEGIN ###
{% extends "demo/chat_home.html" %}
{% load markdown %}

{% block message_list %}
  <div id="messages-container" class="d-flex flex-column">
    <!-- Django alert messages from django.contrib.messages: -->
    {% if messages %}
    <div class="alert-messages">
        {% for message in messages %}
        <div class="alert alert-warning">{{ message }}</div>
        {% endfor %}
    </div>
    {% endif %}

    <div id="messages-list" class="overflow-auto">
      {% for message in thread_messages %}
        <div class="d-flex flex-column p-2">
          <span>
            <strong>
              {% if message.type == "ai" %}AI{% else %}User{% endif %}
            </strong>
          </span>
          <span>{{ message.content|markdown }}</span>
        </div>
      {% endfor %}
    </div>

    <div class="text-center my-2" data-loading>
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div class="d-flex align-items-center mt-auto">
      <textarea
        id="input-area"
        class="form-control"
        placeholder="Enter user message… (Ctrl↵ to send)"
        name="content"
        data-loading-disable
      ></textarea>
      <button
        id="send-message-button"
        class="btn btn-primary ms-3 d-inline-flex align-items-center"
        hx-post="{% url 'chat_thread' thread_id %}"
        hx-include="#input-area"
        hx-target="#messages-container"
        hx-swap="outerHTML"
        hx-select="#messages-container"
        data-loading-disable
      >
        Send <i class="bi bi-send ms-2"></i>
      </button>
    </div>
  </div>
{% endblock %}

### apps/demo/templates/demo/chat_thread.html END ###

### apps/demo/templates/demo/chat_home.html BEGIN ###
{% extends "demo/htmx_index.html" %}

{% block body %}
  <div class="d-flex vh-100">
    <aside class="h-100 col-3 border-right p-3 bg-light">
      <h3>Threads</h3>

        <div id="threads-wrapper" hx-swap-oob="true">
        {% block threads_list %}
          <div id="threads-container" class="d-flex flex-column">
            <div id="threads-list" class="list-group flex-grow-1 overflow-auto">
              {% for thread in threads %}
                <a
                  class="thread-item list-group-item list-group-item-action {% if thread.id == thread_id %}active{% endif %}"
                  href="{% url 'chat_thread' thread.id %}"
                  hx-get="{% url 'chat_thread' thread.id %}"
                  hx-target="#messages-wrapper"
                  hx-select="#messages-wrapper"
                  hx-push-url="true"
                >
                  {{ thread.name }}
                </a>
              {% endfor %}
            </div>

            <button
              id="create-thread-button"
              class="btn btn-primary mt-3"
              hx-post='{% url "chat_home" %}'
              hx-target="#threads-container"
              hx-select="#messages-list"
              hx-select-oob="#messages-list"
              hx-push-url="true"
              data-loading-disable
            >
              Create Thread
            </button>
          </div>
        {% endblock %}
      </div>
    </aside>

    <main class="h-100 col-9 d-flex flex-column p-3 mx-auto main-container">
      <h2 class="mb-4">Chat</h2>

      <div id="messages-wrapper"  hx-swap-oob="true">
        {% block message_list %}
          <div class="text-center text-muted my-3">
            Select or create a thread to start chatting.
          </div>
        {% endblock %}
      </div>
    </main>
  </div>
{% endblock %}

### apps/demo/templates/demo/chat_home.html END ###

### apps/demo/templates/demo/htmx_index.html BEGIN ###
{% load static %}

<!DOCTYPE html>
<html>
  <head>
    <title>Chat Threads</title>
    <link rel="stylesheet" href="{% static 'css/htmx_index.css' %}" />
    <!-- Bootstrap -->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"
      rel="stylesheet"
    />
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.3/js/bootstrap.min.js"></script>
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@2.0.0/dist/htmx.min.js"></script>
    <script src="https://unpkg.com/htmx-ext-loading-states@2.0.0/loading-states.js"></script>
  </head>

  <body
    hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
    hx-ext="loading-states"
  >
    {% block body %}{% endblock %}
  </body>
  <script>
    // Send message on Ctrl+Enter
    document.addEventListener("keydown", function (event) {
      if (event.ctrlKey && event.key === "Enter") {
        document.getElementById("send-message-button").click();
      }
    });
  </script>
</html>

### apps/demo/templates/demo/htmx_index.html END ###

### apps/demo/templates/demo/react_index.html BEGIN ###
{% extends "base.html" %} {% load render_bundle from webpack_loader %} {% block content %}
<div id="react-app"></div>
{% render_bundle 'main' 'js' %} {% endblock %}

### apps/demo/templates/demo/react_index.html END ###

### qa/apps_practice_views_msb_temp.py BEGIN ###
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
import random
import json
import time
import logging
import subprocess
import tempfile
import os
import signal
import sys
from datetime import datetime
import asyncio
from microsandbox import PythonSandbox

from apps.authentication.authentication import JWTOnlyAuthentication
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt
from .serializers import (
    UserStatsSerializer, QuestionSerializer, CodeSubmissionSerializer,
    CodeExecutionSerializer, GradeFeedbackSerializer, AttemptHistorySerializer
)
from .grading import PythonGradingEngine

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get or create user progress statistics."""
    try:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
        )
        
        if created:
            logger.info(f"Created new UserProgress for user: {request.user.username}")
        
        serializer = UserStatsSerializer(user_progress)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return Response(
            {'error': 'Failed to retrieve user statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    """Get the next question based on user's current level."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
        )
        
        # Get questions at the user's current level
        questions = PythonProgrammingQuestion.objects.filter(
            difficulty_level=user_progress.current_level
        )
        
        # Get IDs of questions the user has already attempted
        attempted_question_ids = UserQuestionAttempt.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)
        
        # Filter out attempted questions
        available_questions = questions.exclude(id__in=attempted_question_ids)
        
        # If no new questions at current level, get any question at that level
        if not available_questions.exists():
            available_questions = questions
        
        # If still no questions, expand to nearby levels
        if not available_questions.exists():
            nearby_levels = [
                user_progress.current_level - 1,
                user_progress.current_level + 1
            ]
            available_questions = PythonProgrammingQuestion.objects.filter(
                difficulty_level__in=[l for l in nearby_levels if 1 <= l <= 5]
            ).exclude(id__in=attempted_question_ids)
        
        if available_questions.exists():
            # Select a random question
            question = random.choice(available_questions)
            serializer = QuestionSerializer(question)
            
            # Include user stats in response
            stats_serializer = UserStatsSerializer(user_progress)
            
            return Response({
                'question': serializer.data,
                'user_stats': stats_serializer.data
            })
        else:
            return Response(
                {'error': 'No questions available at your level'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error getting next question: {e}")
        return Response(
            {'error': 'Failed to retrieve next question'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def submit_solution(request):
    """Submit a solution for grading."""
    serializer = CodeSubmissionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        question_id = serializer.validated_data['question_id']
        code = serializer.validated_data['code']
        
        # Get the question
        question = PythonProgrammingQuestion.objects.get(id=question_id)
        
        # Get user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
        )
        
        # Simulate test execution results
        # In a real implementation, this would come from the frontend after Brython execution
        # For now, we'll create mock test results
        test_results = run_test_cases(code, question)
        execution_time = test_results.get('execution_time', 0.1)
        
        # Grade the submission
        grading_engine = PythonGradingEngine()
        grade, feedback = grading_engine.grade_submission(
            code=code,
            expected_output=question.output,
            test_results=test_results,
            execution_time=execution_time
        )
        
        # Save the attempt
        attempt = UserQuestionAttempt.objects.create(
            user=request.user,
            question=question,
            submitted_code=code,
            grade=grade,
            execution_time=execution_time,
            test_results=test_results,
            feedback=feedback
        )
        
        # Update user progress
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += grade
        
        # Increment correct answers count for grades 7-10
        if grade >= 7:
            user_progress.correct_answers_count += 1
        
        user_progress.update_level(grade)
        
        level_changed = old_level != user_progress.current_level
        
        # Prepare response
        response_data = {
            'grade': grade,
            'feedback': feedback,
            'test_results': test_results,
            'execution_time': execution_time,
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None
        }
        
        response_serializer = GradeFeedbackSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data)
        else:
            return Response(response_data)
            
    except PythonProgrammingQuestion.DoesNotExist:
        return Response(
            {'error': 'Question not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error submitting solution: {e}")
        return Response(
            {'error': 'Failed to submit solution'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_attempt_history(request):
    """Get user's attempt history."""
    try:
        attempts = UserQuestionAttempt.objects.filter(
            user=request.user
        ).order_by('-attempted_at')[:20]  # Last 20 attempts
        
        serializer = AttemptHistorySerializer(attempts, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error getting attempt history: {e}")
        return Response(
            {'error': 'Failed to retrieve attempt history'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def run_test_cases(code: str, question: PythonProgrammingQuestion) -> dict:
    """
    Mock function to simulate running test cases.
    In production, this would be replaced with actual test execution
    from the frontend using Brython.
    """
    # This is a simplified mock - the real execution happens in the frontend
    # The frontend will send back the actual test results
    
    # For now, return mock results based on simple heuristics
    has_function = 'def ' in code
    has_return = 'return' in code or 'print' in code
    
    if not has_function or not has_return:
        return {
            'total': 5,
            'passed': 0,
            'failed': 5,
            'execution_time': 0.01,
            'failed_tests': [
                {'name': 'test_basic', 'error': 'No output produced'},
                {'name': 'test_empty', 'error': 'No output produced'},
            ]
        }
    
    # Simulate varying success rates
    import random
    passed = random.randint(2, 5)
    
    return {
        'total': 5,
        'passed': passed,
        'failed': 5 - passed,
        'execution_time': random.uniform(0.01, 0.5),
        'failed_tests': [
            {'name': f'test_{i}', 'error': 'Output mismatch'}
            for i in range(5 - passed)
        ] if passed < 5 else []
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_python_code(request):
    """
    Execute Python code on the backend and return the output without submission (for testing)
    """
    code = request.data.get('code', '').strip()
    if not code:
        return Response({
            'output': '',
            'error': 'No code provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    async def execute_code():
        try:
            async with PythonSandbox.create(name=f"user_{request.user.id}") as sandbox:
                # Set a 10-second timeout for the entire execution
                async with asyncio.timeout(10):
                    exec_result = await sandbox.run(code)
                    output = await exec_result.output()
                    return output, None
        except asyncio.TimeoutError:
            return '', 'Code execution timed out (10 seconds limit)'
        except Exception as e:
            return '', f'Execution error: {str(e)}'
    
    try:
        # Run the async code in the sync Django view
        output, error = asyncio.run(execute_code())
        
        return Response({
            'output': output,
            'error': error,
            'execution_time': datetime.now().isoformat()
        })
    
    except Exception as e:
        return Response({
            'output': '',
            'error': f'Setup error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### qa/apps_practice_views_msb_temp.py END ###

### qa/bugs/.gitkeep BEGIN ###

### qa/bugs/.gitkeep END ###

### qa/template/bug_report.md BEGIN ###
Bug Report
Context:

Expected vs. Actual Behavior

Expected:

Actual:

Steps to Reproduce:
1.
2.

Frequency:

Additional Details:

Log:

Instructions:
This might be a complex bug, so let's divide it into steps.
1. Consider and understand what led to the bug and consider possible issues.
2. Inspect the relevant code thoroughly to understand your assumptions.
3. If you have understood the source of the bug, fix it.
### qa/template/bug_report.md END ###

### planning/process_flow.mermaid BEGIN ###
graph TB
    %% Define styles
    classDef userAction fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
    classDef systemAction fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef database fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef decision fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef ui fill:#fce4ec,stroke:#e91e63,stroke-width:2px

    %% Main Flow
    Start([User Enters Practice Screen]):::userAction
    
    %% Initial Setup
    Start --> GetUserData[(Retrieve User Data from DB)]:::database
    GetUserData --> Greet[System Greets User by Name]:::systemAction
    Greet --> GetInitialQ[(Get Level 3 Question from DB)]:::database
    GetInitialQ --> DisplayQ[Display Question in Chat UI]:::ui
    
    %% Coding Process
    DisplayQ --> CodeWrite[User Writes Code in Editor]:::userAction
    CodeWrite --> TestCode[User Tests Code Output]:::userAction
    TestCode --> ViewOutput[View Results in Output Panel]:::ui
    ViewOutput --> MoreTests{Need More Testing?}:::decision
    MoreTests -->|Yes| CodeWrite
    MoreTests -->|No| Submit[User Clicks Submit]:::userAction
    
    %% Assessment Process
    Submit --> GetSolution[(Retrieve Solution from DB)]:::database
    GetSolution --> Assess[Assessment Engine Evaluates Code]:::systemAction
    Assess --> Metrics[Apply Multiple Assessment Metrics:<br/>- Correctness<br/>- Time Complexity<br/>- Space Complexity<br/>- Code Quality]:::systemAction
    Metrics --> GenFeedback[Generate Detailed Feedback]:::systemAction
    GenFeedback --> DisplayFeedback[Display Feedback in Chat UI]:::ui
    
    %% Performance Tracking
    DisplayFeedback --> UpdatePerf[Update Performance Record]:::systemAction
    UpdatePerf --> CheckConsec{Check Consecutive<br/>Wins/Failures}:::decision
    
    %% Level Adjustment Logic
    CheckConsec -->|2 Consecutive Wins| LevelUp[Move User Up One Level]:::systemAction
    CheckConsec -->|2 Consecutive Failures| LevelDown[Move User Down One Level]:::systemAction
    CheckConsec -->|Mixed Results| StayLevel[Stay at Current Level]:::systemAction
    
    %% Next Question Selection
    LevelUp --> UpdateLevel[(Update User Level in DB)]:::database
    LevelDown --> UpdateLevel
    StayLevel --> UpdateLevel
    UpdateLevel --> GetNextQ[(Get Next Question for User's Level)]:::database
    GetNextQ --> DisplayNext[Display Next Question]:::ui
    
    %% Continue Loop
    DisplayNext --> ContinuePractice{Continue Practicing?}:::decision
    ContinuePractice -->|Yes| CodeWrite
    ContinuePractice -->|No| End([End Session]):::userAction
    
    %% Subgraphs for clarity
    subgraph "User Interface"
        DisplayQ
        ViewOutput
        DisplayFeedback
        DisplayNext
    end
    
    subgraph "Assessment System"
        Assess
        Metrics
        GenFeedback
    end
    
    subgraph "Level Management"
        CheckConsec
        LevelUp
        LevelDown
        StayLevel
    end
### planning/process_flow.mermaid END ###

### tests/test_db_connection.py BEGIN ###
import os
import django
import sys

# Add the parent directory to Python path to import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from django.contrib.auth.models import User

def test_db_connection():
    try:
        # Try to get all users
        users = User.objects.all()
        
        print("Database connection successful!")
        print("\nList of users in the database:")
        print("-" * 50)
        
        if users.exists():
            for user in users:
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Date joined: {user.date_joined}")
                print("-" * 50)
        else:
            print("No users found in the database.")
            
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    test_db_connection()

### tests/test_db_connection.py END ###

### tests/test_grading_details.py BEGIN ###
#!/usr/bin/env python
"""Detailed test to understand grading breakdown."""

import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.practice.grading import PythonGradingEngine
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion

def test_detailed_grading():
    """Test grading with detailed breakdown."""
    engine = PythonGradingEngine()
    
    # Create a mock question
    mock_question = type('MockQuestion', (), {
        'instruction': 'Test instruction',
        'input': 'Test input',
        'output': 'Test output'
    })()
    
    # Test minimal code
    code = 'x = 1'
    
    # Mock test results - all tests fail
    mock_test_results = {
        'total': 5,
        'passed': 0,
        'failed': 5,
        'execution_time': 0.1,
        'failed_tests': []
    }
    
    print("Testing minimal code: 'x = 1'")
    print("All tests fail (0/5 passed)\n")
    
    grade, feedback = engine.grade_submission(
        code=code,
        question=mock_question,
        test_results=mock_test_results,
        execution_time=0.1
    )
    
    print(f"Grade: {grade}")
    print("\nDetailed scores:")
    print(f"Correctness: {feedback['correctness'].get('score', 0):.2f} (weight: 0.4)")
    print(f"Code Quality: {feedback['code_quality'].get('score', 0):.2f} (weight: 0.3)")
    print(f"Efficiency: {feedback['efficiency'].get('score', 0):.2f} (weight: 0.2)")
    print(f"Sophistication: {feedback['sophistication'].get('score', 0):.2f} (weight: 0.1)")
    
    # Calculate weighted score manually
    weighted = (
        feedback['correctness'].get('score', 0) * 0.4 +
        feedback['code_quality'].get('score', 0) * 0.3 +
        feedback['efficiency'].get('score', 0) * 0.2 +
        feedback['sophistication'].get('score', 0) * 0.1
    )
    print(f"\nWeighted score: {weighted:.4f}")
    print(f"Expected grade (ceil({weighted:.4f} * 10)): {int(weighted * 10) + (1 if (weighted * 10) % 1 > 0 else 0)}")
    
    # Test with syntax error
    print("\n" + "="*50)
    print("\nTesting code with syntax error:")
    bad_code = 'def test(\n    return'
    
    grade2, feedback2 = engine.grade_submission(
        code=bad_code,
        question=mock_question,
        test_results=mock_test_results,
        execution_time=0.1
    )
    
    print(f"Grade: {grade2}")
    print(f"Code Quality score: {feedback2['code_quality'].get('score', 0):.2f}")

if __name__ == '__main__':
    test_detailed_grading() 
### tests/test_grading_details.py END ###

### tests/test_grading_changes.py BEGIN ###
#!/usr/bin/env python
"""Test script to verify grading changes for grade 0 implementation."""

import os
import sys
import django

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project root to the Python path
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.practice.grading import PythonGradingEngine

def test_grading_engine():
    """Test the grading engine with various code submissions."""
    engine = PythonGradingEngine()
    
    # Test cases
    test_cases = [
        {
            'name': 'Empty code',
            'code': '',
            'expected_grade': 0
        },
        {
            'name': 'Only whitespace',
            'code': '   \n\t  \n   ',
            'expected_grade': 0
        },
        {
            'name': 'Only single-line comments',
            'code': '# This is a comment\n# Another comment',
            'expected_grade': 0
        },
        {
            'name': 'Only multi-line comments',
            'code': '"""\nThis is a docstring\n"""\n# And a comment',
            'expected_grade': 0
        },
        {
            'name': 'Minimal code (should get grade 1)',
            'code': 'x = 1',
            'expected_grade': 1
        },
        {
            'name': 'Code with comments',
            'code': '# This is a comment\nx = 1  # inline comment',
            'expected_grade': 1
        },
        {
            'name': 'Function with no tests passing',
            'code': 'def solution():\n    return None',
            'expected_grade': 1
        }
    ]
    
    # Mock test results for non-empty code
    mock_test_results = {
        'total': 5,
        'passed': 0,
        'failed': 5,
        'execution_time': 0.1,
        'failed_tests': []
    }
    
    print("Testing grading engine with new grade 0 logic:\n")
    
    for test in test_cases:
        grade, feedback = engine.grade_submission(
            code=test['code'],
            expected_output='',
            test_results=mock_test_results,
            execution_time=0.1
        )
        
        status = "✓" if grade == test['expected_grade'] else "✗"
        print(f"{status} {test['name']}: Expected grade {test['expected_grade']}, got grade {grade}")
        
        if grade != test['expected_grade']:
            print(f"  Feedback: {feedback.get('overall', 'No overall feedback')}")
    
    print("\nTesting ceil function behavior:")
    # Test ceil function with different weighted scores
    test_scores = [0.0001, 0.1, 0.11, 0.49, 0.5, 0.91, 0.99]
    for score in test_scores:
        # Simulate non-empty code with a specific weighted score
        # We need to manipulate the grading internals for this test
        expected_grade = int(score * 10) + (1 if (score * 10) % 1 > 0 else 0)
        if score == 0:
            expected_grade = 1  # Minimum for non-empty code
        print(f"  Weighted score {score:.4f} should give grade {expected_grade}")

if __name__ == '__main__':
    test_grading_engine() 
### tests/test_grading_changes.py END ###

### tests/test_sample_data.py BEGIN ###
#!/usr/bin/env python3
"""
Sample Data Script

This script demonstrates how to load and sample data from the Python Programming Questions Dataset.
It creates a df_sample dataframe with SAMPLE_SIZE sampled questions.

Usage:
    python test_sample_data.py
"""
import sys
import pandas as pd
import logging
from pathlib import Path

#CSV_FILE_PATH = "data/Python Programming Questions Dataset.csv"
#SAMPLE_SIZE = 10

CSV_FILE_PATH = "data/sample_questions.csv"
SAMPLE_SIZE = 5

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from apps.instructions_difficulty_eval.data_processor import DataProcessor

# Configure Django environment for logging
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

# Django logging configuration is already set up via settings.py

logger = logging.getLogger(__name__)


def create_sample_dataframe(csv_path: str = CSV_FILE_PATH, 
                          sample_size: int = SAMPLE_SIZE) -> pd.DataFrame:
    """
    Create a sample dataframe from the Python Programming Questions Dataset.
    
    Args:
        csv_path (str): Path to the CSV file
        sample_size (int): Number of questions to sample
        
    Returns:
        pd.DataFrame: Sampled dataframe (df_sample)
    """
    try:
        # Initialize data processor
        processor = DataProcessor(csv_path)
        
        # Load and sample data
        df_sample = processor.sample_questions(n=sample_size, random_state=42)
        
        logger.info(f"Created df_sample with {len(df_sample)} questions")
        logger.info(f"Columns: {list(df_sample.columns)}")
        logger.info(f"Sample shape: {df_sample.shape}")
        
        return df_sample
        
    except Exception as e:
        logger.error(f"Error creating sample dataframe: {e}")
        raise


def display_sample_info(df_sample: pd.DataFrame) -> None:
    """
    Display information about the sampled dataframe.
    
    Args:
        df_sample (pd.DataFrame): The sampled dataframe
    """
    print("="*60)
    print("SAMPLE DATAFRAME INFORMATION")
    print("="*60)
    print(f"Shape: {df_sample.shape}")
    print(f"Columns: {list(df_sample.columns)}")
    print(f"Memory usage: {df_sample.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print("\nFirst 3 sample instructions:")
    print("-" * 40)
    for i, instruction in enumerate(df_sample['Instruction'].head(3), 1):
        print(f"{i}. {instruction[:100]}...")
    
    print("\nData types:")
    print("-" * 20)
    print(df_sample.dtypes)
    
    print("\nMissing values:")
    print("-" * 20)
    print(df_sample.isnull().sum())


def main():
    """
    Main function to demonstrate data sampling.
    """
    try:
        # Create sample dataframe
        df_sample = create_sample_dataframe()
        
        # Display information
        display_sample_info(df_sample)
        
        # Save sample to CSV for inspection
        output_path = "data/sample_questions_output.csv"
        df_sample.to_csv(output_path, index=False)
        print(f"\nSample saved to: {output_path}")
        
        print("\n" + "="*60)
        print("Sample dataframe created successfully!")
        print("You can now use 'df_sample' for further processing.")
        print("="*60)
        
        return df_sample
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    df_sample = main() 
### tests/test_sample_data.py END ###

### operations/git/set_git_remote.sh BEGIN ###
git remote add origin https://github.com/ronister/ai_interview_preparation_platform.git
git remote set-url origin https://github.com/ronister/ai_interview_preparation_platform.git
### operations/git/set_git_remote.sh END ###

### operations/git/reconcile_branches_config.sh BEGIN ###
git config pull.rebase false
### operations/git/reconcile_branches_config.sh END ###

### operations/git/set_git_email_and_user.sh BEGIN ###
git config user.email 'roni.shternberg@gmail.com'
git config user.name 'Roni Shternberg'
### operations/git/set_git_email_and_user.sh END ###

### DIRECTORY PROJECT_ROOT FLATTENED CONTENT ###
