# Adaptive Python Interview Preparation Platform using AI Agents  (🚀)

✨ Key Features
* Smart Question Engine – serves problems that match your skill level

* Auto-grader – runs code, scores correctness + code quality + efficiency + sophistication

* Progress Stats – track average grade and success rate

## 🚀 Quick Start

### Prerequisites
- PostgreSQL installed and configured
- Python with Poetry (recommended with pyenv)
- Node.js and Yarn

### Setup Instructions

1. **Database Setup**
   - Create a PostgreSQL database
   - Configure database name and credentials in `env/.env` (see `.env.example`)

2. **Environment Configuration**
   ```bash
   # Set your Claude API key in env/.env
   CLAUDE_API_KEY=your_api_key_here
   ```

3. **Backend Setup**
   ```bash
   # Install Python dependencies
   poetry install
   
   # Activate virtual environment
   . .venv/bin/activate
   
   # Run Django migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Initialize difficulty evaluation (~$5 cost)
   python instructions_difficulty_eval.py
   ```

4. **Frontend Setup**
   ```bash
   # Install Node.js dependencies
   yarn install
   ```

5. **Start the Application**
   ```bash
   # Run backend, frontend and optionally microsandbox
   sh runs.sh
   ```

6. **Access the Platform**
   - Open [http://localhost:8000](http://localhost:8000) and start practicing!


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