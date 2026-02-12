# Session lifecycle

This project uses a strict single-session model:

- Launch browser once
- Create one context
- Use one page
- Process all identifiers sequentially
- Close browser at the end

Any unexpected UI state triggers an immediate abort with non-zero exit.
