# Contributing to Betting Simulation Platform

Thank you for your interest in contributing to the Betting Simulation Platform! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Set up the development environment** following the instructions in the README.md
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Setting Up

1. Make sure you have Python 3.x and all dependencies installed
2. Create and activate a virtual environment
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Making Changes

1. **Follow the coding style** of the project (PEP 8 for Python)
2. **Write or update tests** for the changes you make
3. **Run tests** to ensure your changes don't break existing functionality:
   ```bash
   python manage.py test
   ```
4. **Document your changes** in the code and update documentation files if necessary

### Submitting Changes

1. **Commit your changes** with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Create a Pull Request** from your fork to the main repository
4. **Describe your changes** in the Pull Request description, including the motivation and context

## Code Style and Standards

- Follow **PEP 8** guidelines for Python code
- Use **meaningful variable and function names**
- Add **docstrings** to all functions, classes, and modules
- Keep functions **focused on a single responsibility**
- Write **clear, concise comments** explaining complex logic

## Testing

- Add tests for all new features or bug fixes
- Ensure all tests pass before submitting a Pull Request
- Aim for high test coverage

## Documentation

- Update the README.md if you change functionality
- Document new features in the appropriate sections
- Create or update API documentation if applicable

## Feature Requests and Bug Reports

- Use the **Issues** section on GitHub to report bugs or suggest features
- Include detailed information on how to reproduce bugs
- For feature requests, explain the use case and benefits

## Areas for Contribution

- Implementing new betting strategies
- Improving the UI/UX
- Enhancing visualization capabilities
- Adding data export options
- Optimizing simulation performance
- Improving test coverage
- Enhancing documentation

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have any questions or need help, feel free to create an issue or reach out to the project maintainers.

Thank you for contributing to make the Betting Simulation Platform better! 