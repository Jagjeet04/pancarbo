# Contributing to Pancarbo Greenfuels

Thank you for your interest in contributing! We welcome contributions from everyone.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive.

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Describe the bug with as much detail as possible
- Include steps to reproduce
- Include expected vs actual behavior
- Attach screenshots if applicable

### Suggesting Enhancements

- Use the GitHub issue tracker
- Clear description of the enhancement
- Explain the use case and benefits
- Provide examples of how it would work

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Ensure code quality:
   ```bash
   flake8 .
   pytest
   ```
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Pancarbo-Greenfuels-AI-System.git
cd Pancarbo-Greenfuels-AI-System

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```

## Code Style Guidelines

- Follow PEP 8
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Add type hints where possible

Example:
```python
def calculate_efficiency(temperature: float, steam_output: float) -> float:
    """
    Calculate boiler efficiency based on parameters.
    
    Args:
        temperature: Operating temperature in Celsius
        steam_output: Steam output in tph
        
    Returns:
        Efficiency as a percentage (0.0 - 1.0)
    """
    optimal_temp = 900
    optimal_steam = 30
    temp_eff = 1 - abs(temperature - optimal_temp) / optimal_temp
    steam_eff = 1 - abs(steam_output - optimal_steam) / optimal_steam
    return (temp_eff + steam_eff) / 2
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
pytest --cov=. --cov-report=term-missing
```

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update configuration docs if adding settings
- Include examples for complex features

## Commit Messages

Use clear, descriptive commit messages:

- ✨ `:sparkles:` - New feature
- 🐛 `:bug:` - Bug fix
- 📚 `:books:` - Documentation
- ♻️ `:recycle:` - Refactoring
- ✅ `:white_check_mark:` - Tests
- 🎨 `:art:` - Style changes

Example:
```
✨ Add SHAP explainability module

- Implement SHAP force plots
- Add feature importance visualization
- Update documentation
```

## Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure CI/CD passes
4. Request review from maintainers
5. Address feedback
6. Merge when approved

## Questions?

- Open an issue with your question
- Join our discussions
- Email: team@pancarbo.com

## License

By contributing, you agree your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Pancarbo Greenfuels!**
