# reqtracker Examples

This directory contains practical examples demonstrating how to use reqtracker in different scenarios and project types.

---

## 📁 Directory Structure

### 🚀 Basic Examples (`basic/`)
- **simple_usage.py** - Basic Python library usage
- **cli_examples.sh** - Essential CLI commands

### 🌐 Web Development (`web_development/`)
- **django_project.py** - Django project dependency tracking
- **flask_app.py** - Flask application analysis

### 📊 Data Science (`data_science/`)
- **jupyter_notebooks.py** - Notebook dependency management

### ⚙️ Advanced Usage (`advanced/`)
- **custom_config.py** - Advanced configuration examples
- **github_actions.yml** - GitHub Actions workflow example
- **gitlab_ci.yml** - GitLab CI/CD pipeline example
- **Jenkinsfile** - Jenkins Pipeline example

### 📋 Configuration Examples (`config_examples/`)
- **basic.reqtracker.toml** - Basic configuration file
- **django.reqtracker.toml** - Django-specific settings
- **data_science.reqtracker.toml** - Data science project config

---

## 🚀 Quick Start

### Run Any Example
```bash
# Navigate to examples directory
cd examples

# Run basic usage example
python basic/simple_usage.py

# Execute CLI examples
bash basic/cli_examples.sh

# Try advanced configuration
python advanced/custom_config.py
```

### Use Configuration Examples

```bash
# Copy a config template to your project
cp config_examples/basic.reqtracker.toml /path/to/your/project/.reqtracker.toml

# Use specific config with reqtracker
reqtracker analyze --config config_examples/django.reqtracker.toml
```

### Use CI/CD Examples

```bash
# For GitHub Actions
cp advanced/github_actions.yml /path/to/your/project/.github/workflows/update-requirements.yml

# For GitLab CI
cp advanced/gitlab_ci.yml /path/to/your/project/.gitlab-ci.yml

# For Jenkins
cp advanced/Jenkinsfile /path/to/your/project/Jenkinsfile
```

---

## 📖 Learning Path

1. **Start with basics** - `basic/simple_usage.py`
2. **Try CLI commands** - `basic/cli_examples.sh`
3. **Explore your use case**:
   - Web developers → `web_development/`
   - Data scientists → `data_science/`
   - Advanced users → `advanced/`
4. **Customize configuration** - `config_examples/`
5. **Set up CI/CD** - Choose from `advanced/` CI/CD examples

---

## 🤔 Need Help?

- Check the main [README.md](../README.md) for complete documentation
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
- Open an [issue](https://github.com/oleksii-shcherbak/reqtracker/issues) for questions
