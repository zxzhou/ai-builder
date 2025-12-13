# Setup Instructions

## Environment Variable Setup

1. Create a `.env.local` file in the project root directory (`project-8/`)

2. Add the following line to `.env.local`:
   ```
   AI_BUILDER_TOKEN=sk_888fcdbf_e778e006fa20495392c24c45cabed3bba245
   ```

3. **Important**: The `.env.local` file is already in `.gitignore`, so it won't be committed to version control.

4. Restart your development server after creating or modifying `.env.local`

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at http://localhost:3000

## Troubleshooting

If you see errors about `AI_BUILDER_TOKEN`:
- Make sure `.env.local` exists in the `project-8/` directory (not in a parent directory)
- Verify the file contains exactly: `AI_BUILDER_TOKEN=your_token_here` (no quotes, no spaces around the `=`)
- Restart the development server after creating/modifying the file

