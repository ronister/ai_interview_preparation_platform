# Adaptive Python Interview Preparation Platform using AI Agents  (🚀)

✨ Key Features
* Smart Question Engine – serves problems that match your skill level

* Auto-grader – runs code, scores correctness + code quality + efficiency + sophistication

* Progress Stats – track average grade and success rate

* Procedure:
- Install and configure PostgreSQL
- create database (name and credentials should be in env/.env, see: .env.example)
- Set CLAUDE_API_KEY (in env/.env)
- Run:
    $ poetry install (recommended with pyenv)
    $ . .venv/bin/activate
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python instructions_difficulty_eval.py (~5$ cost)
    $ yarn install (Node JS)
    $ sh runs.sh (runs backend, frontend and optionally microsandbox)

- Open http://localhost:8000 and start practicing!


Tech Stack
WSL • Django • Claude LLM • React + TypeScript • PostgreSQL • LangChain • django-ai-assistant 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* [django-ai-assistant](https://github.com/vintasoftware/django-ai-assistant) - AI assistant integration for Django

📧 Contact
Project Author: Roni Shternberg
GitHub: @ronister 
Email: roni.shternberg@gmail.com

Happy coding & good luck with your next Python interview!