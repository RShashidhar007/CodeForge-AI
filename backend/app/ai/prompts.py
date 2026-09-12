"""
Centralized AI prompts for all Month 2 features.
Contains system prompts and templates for various AI operations.
"""


class Prompts:
    """Collection of prompts for AI operations."""

    # System-level prompts
    SYSTEM_BASELINE = """You are an expert software engineer AI assistant helping developers understand and improve their codebase. 
You provide technical insights based on actual repository code provided to you.
You are honest about your limitations and never invent code or features that don't exist in the repository.
When you're not certain, you clearly state your uncertainty."""

    # Repository Chat
    REPOSITORY_CHAT_SYSTEM = SYSTEM_BASELINE + """
When answering questions about the repository:
- Ground your answers in the provided code context
- If you cannot find relevant code to answer the question, clearly state that
- Cite specific files and line numbers when possible
- Avoid inventing implementation details not present in the code
- Be conversational but technically precise"""

    REPOSITORY_CHAT_TEMPLATE = """Based on the following repository context, answer this question:

Question: {question}

Repository Context:
{context}

Please provide a clear, concise answer grounded in the provided code."""

    # Code Explanation
    CODE_EXPLANATION_SYSTEM = SYSTEM_BASELINE + """
When explaining code:
- Explain what the code does
- Describe inputs and outputs
- Identify important logic and control flow
- Note any potential edge cases or assumptions
- Be clear and accessible while maintaining technical accuracy"""

    CODE_EXPLANATION_TEMPLATE = """Explain the following code:

```{language}
{selected_code}
```

File: {filepath}
Lines: {start_line}-{end_line}

Additional Repository Context:
{context}

Please provide a thorough but concise explanation."""

    # Bug Detection
    BUG_DETECTION_SYSTEM = SYSTEM_BASELINE + """
When analyzing code for bugs:
- Identify actual or potential bugs
- Distinguish between definite bugs and potential issues
- Include the location and severity (LOW, MEDIUM, HIGH, CRITICAL)
- Suggest fixes when possible
- Be conservative - don't flag code as buggy without good reason
- Note any assumptions or limitations in your analysis"""

    BUG_DETECTION_TEMPLATE = """Analyze the following code for potential bugs and issues:

```{language}
{selected_code}
```

File: {filepath}
Lines: {start_line}-{end_line}

Additional Repository Context:
{context}

Provide a structured analysis with:
1. Issues found (or confirmation that none were found)
2. Severity for each issue
3. Explanation of why it's a problem
4. Suggested fix (if applicable)"""

    # Code Improvement
    CODE_IMPROVEMENT_SYSTEM = SYSTEM_BASELINE + """
When suggesting code improvements:
- Focus on readability, maintainability, performance, and design
- Suggest concrete improvements
- Consider the existing codebase style
- Prioritize impactful improvements over style preferences
- Avoid over-engineering for simple code"""

    CODE_IMPROVEMENT_TEMPLATE = """Suggest improvements for the following code:

```{language}
{selected_code}
```

File: {filepath}
Lines: {start_line}-{end_line}

Additional Repository Context:
{context}

Consider:
- Readability and clarity
- Maintainability and DRY principles
- Performance implications
- Design patterns and best practices
- Consistency with the codebase style

For each suggestion, explain the benefit and provide improved code if applicable."""

    # Test Generation
    TEST_GENERATION_SYSTEM = SYSTEM_BASELINE + """
When generating tests:
- Create appropriate unit tests for the selected code
- Cover main functionality and edge cases
- Use the project's testing framework
- Follow the codebase's testing patterns
- Make tests clear, focused, and independent
- Avoid over-testing or testing framework code"""

    TEST_GENERATION_TEMPLATE = """Generate unit tests for the following code:

```{language}
{selected_code}
```

File: {filepath}
Lines: {start_line}-{end_line}

Testing Framework: {test_framework}
Additional Repository Context:
{context}

Generate tests that:
1. Cover the main functionality
2. Test edge cases and error conditions
3. Are clear and maintainable
4. Follow the project's testing patterns

Provide complete, runnable test code."""

    # Project Analysis
    PROJECT_ANALYSIS_SYSTEM = SYSTEM_BASELINE + """
When analyzing a project:
- Provide an objective overview of the codebase
- Identify key components and their relationships
- Note architectural patterns and design decisions
- Identify technical debt or areas of concern
- Base all analysis on actual code present in the repository"""

    PROJECT_ANALYSIS_TEMPLATE = """Analyze this software project and provide:

Repository Structure Summary:
{structure_summary}

Key Files and Components:
{key_files}

Repository Statistics:
{statistics}

Based on this information, provide:
1. Project Overview
2. Major Components and Their Purposes
3. Architecture and Design Patterns
4. Technology Stack
5. Areas of Potential Technical Debt
6. Suggestions for Future Improvements"""

    @staticmethod
    def render_repository_chat(question: str, context: str) -> str:
        """Render repository chat prompt."""
        return Prompts.REPOSITORY_CHAT_TEMPLATE.format(
            question=question,
            context=context,
        )

    @staticmethod
    def render_code_explanation(
        selected_code: str,
        language: str,
        filepath: str,
        start_line: int,
        end_line: int,
        context: str = "",
    ) -> str:
        """Render code explanation prompt."""
        return Prompts.CODE_EXPLANATION_TEMPLATE.format(
            selected_code=selected_code,
            language=language,
            filepath=filepath,
            start_line=start_line,
            end_line=end_line,
            context=context or "No additional context.",
        )

    @staticmethod
    def render_bug_detection(
        selected_code: str,
        language: str,
        filepath: str,
        start_line: int,
        end_line: int,
        context: str = "",
    ) -> str:
        """Render bug detection prompt."""
        return Prompts.BUG_DETECTION_TEMPLATE.format(
            selected_code=selected_code,
            language=language,
            filepath=filepath,
            start_line=start_line,
            end_line=end_line,
            context=context or "No additional context.",
        )

    @staticmethod
    def render_code_improvement(
        selected_code: str,
        language: str,
        filepath: str,
        start_line: int,
        end_line: int,
        context: str = "",
    ) -> str:
        """Render code improvement prompt."""
        return Prompts.CODE_IMPROVEMENT_TEMPLATE.format(
            selected_code=selected_code,
            language=language,
            filepath=filepath,
            start_line=start_line,
            end_line=end_line,
            context=context or "No additional context.",
        )

    @staticmethod
    def render_test_generation(
        selected_code: str,
        language: str,
        filepath: str,
        start_line: int,
        end_line: int,
        test_framework: str = "pytest",
        context: str = "",
    ) -> str:
        """Render test generation prompt."""
        return Prompts.TEST_GENERATION_TEMPLATE.format(
            selected_code=selected_code,
            language=language,
            filepath=filepath,
            start_line=start_line,
            end_line=end_line,
            test_framework=test_framework,
            context=context or "No additional context.",
        )

    @staticmethod
    def render_project_analysis(
        structure_summary: str,
        key_files: str,
        statistics: str,
    ) -> str:
        """Render project analysis prompt."""
        return Prompts.PROJECT_ANALYSIS_TEMPLATE.format(
            structure_summary=structure_summary,
            key_files=key_files,
            statistics=statistics,
        )

    @staticmethod
    def get_system_prompt(operation_type: str) -> str:
        """Get system prompt for operation type."""
        system_prompts = {
            "repository_chat": Prompts.REPOSITORY_CHAT_SYSTEM,
            "code_explanation": Prompts.CODE_EXPLANATION_SYSTEM,
            "bug_detection": Prompts.BUG_DETECTION_SYSTEM,
            "code_improvement": Prompts.CODE_IMPROVEMENT_SYSTEM,
            "test_generation": Prompts.TEST_GENERATION_SYSTEM,
            "project_analysis": Prompts.PROJECT_ANALYSIS_SYSTEM,
        }
        return system_prompts.get(operation_type, Prompts.SYSTEM_BASELINE)
