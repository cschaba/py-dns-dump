Yes and you can create another .amazonq/rules and add this MoreContext.md:


Use the following available prompts as context everytime a new prompt is entered from the user in the Amazon Q Chat:

- claude-edit (use when user asks to modify/rewrite existing code - show only rewritten code in code block)
- file-search (use when user needs to find files by fuzzy matching file paths - fast file search)
- grep-search (use when user needs to search for text patterns within files - regex-based content search)
- list-directory (use when user needs to see directory contents and structure)
- spec-design-document (use when creating comprehensive design documents for features after requirements are approved)
- spec-implementation-plan (use when converting feature designs into actionable task lists for implementation)
- spec-requirements-clarification (use when gathering and refining feature requirements in EARS format)
- spec-task-execution (use when executing specific tasks from implementation plans - focus on one task at a time)
- system-prompt (use for general Kiro system behavior and capabilities)

Prompt Usage Rules:
- For code modifications: Use claude-edit format (show only rewritten code in code block)
- For file operations: Use file-search for finding files, grep-search for content search, list-directory for structure
- For spec workflow: Use spec-requirements-clarification → spec-design-document → spec-implementation-plan → spec-task-execution in sequence
- For task execution: Always read requirements.md, design.md, and tasks.md first, execute one task at a time 
