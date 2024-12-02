# Contributing to DNA Helix Visualizer

We welcome contributions to the DNA Helix Visualizer project! Here's how you can help.

## Getting Started

1. Fork the repository
2. Create a development environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

##Development Process
1. Create a new branch for your feature: ```bash git checkout -b feature/your-feature-name ```

2. Write your code following these guidelines:
* Use type hints for function parameters
* * Add docstrings for new functions
* Follow PEP 8 style guidelines
* Keep functions focused and single-purpose
3. Test your changes:
* Use the test data generator in tests/
* Verify visualizations work in both static and interactive modes
* Check performance with large datasets 

## Pull Request Process
U1. pdate documentation:
* Add new features to README.md
* Update docstrings and comments
* Include example usage if applicable
2. Submit your PR:
* Reference any related issues
* Provide a clear description of changes
* Include screenshots for visualization changes

## Code Style
* Use 4 spaces for indentation
* Maximum line length: 100 characters
* Group imports in this order: ```python
* Use meaningful variable names that reflect their purpose

## Adding New Features
When adding new visualization types:

* Create a new function in helix_drawer.py
* Add configuration options in DNAConfig
* Update the main processing pipeline
* Add examples to the Jupyter notebook

## Running Tests
Generate test data: ```bash python3 -m tests.generate_test_data ```

## Questions?
Open an issue for:
* Feature proposals
* Bug reports
* Documentation improvements
* General questions

Your contributions make DNA Helix Visualizer better! ```