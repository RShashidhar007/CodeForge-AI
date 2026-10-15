# CodeForge AI - Frontend

Modern React 19 + TypeScript 6 web application for AI-powered coding assessments and interview management.

## Features

### Role-Based Dashboards
- **Candidate Dashboard**: View assigned projects, track progress, and access AI-powered code assistance
- **Recruiter Dashboard**: Create and manage projects, review candidate submissions, and track hiring pipelines
- **Admin Dashboard**: User management, system monitoring, and role assignments

### GitHub OAuth Integration
- Secure authentication via GitHub OAuth 2.0
- Import public and private repositories with one click
- Automatic repository cloning and code indexing for semantic search

### Repository Import & Management
- Real-time import progress tracking with WebSocket updates
- Clone repositories directly from GitHub
- Support for public and private repositories (with authenticated access)
- Automatic code indexing for semantic search and AI chat

### Semantic Code Search
- Vector-based semantic search powered by Qdrant
- Search across all indexed repositories by natural language queries
- View matched code snippets with file paths, line numbers, and symbols
- Context-aware results ranked by relevance

### AI Chat with Code Blocks
- Interactive chat interface for asking questions about your codebase
- Syntax-highlighted code blocks with language detection
- One-click copy-to-clipboard functionality for code snippets
- Message timestamps for conversation tracking
- Source citations linking back to referenced code files
- Conversation history management

## Tech Stack

- **React 19** - Modern UI library with latest hooks and concurrent features
- **TypeScript 6** - Static typing and enhanced developer experience
- **Vite 8** - Lightning-fast build tool and development server
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing and navigation
- **Lucide React** - Beautiful, consistent icon library
- **React Toastify** - Toast notifications for user feedback

## Quick Start

### Prerequisites
- Node.js 18+ and npm 9+
- Backend API running at `http://localhost:8080/api` (or configured endpoint)

### Installation

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`.

## Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Backend API base URL
VITE_API_BASE_URL=http://localhost:8080/api
```

**Note**: Vite only loads environment variables prefixed with `VITE_`. The `.env.local` file is automatically loaded and should never be committed to version control.

## Routes

### Public Routes
- `/login` - User login page
- `/register` - New user registration
- `/github/callback` - GitHub OAuth callback handler

### Protected Routes (Candidate & Recruiter)
- `/dashboard` - Role-specific dashboard (candidate or recruiter view)
- `/profile` - User profile management
- `/github` - GitHub repository import and management
- `/ai/:projectId?` - AI chat and semantic code search interface
  - Optional `projectId` parameter for project-specific context

### Admin Routes
- `/admin/dashboard` - Admin dashboard overview
- `/admin/users` - User management (create, edit, delete, role assignment)

## GitHub OAuth Setup

To enable GitHub authentication:

1. **Create GitHub OAuth App**:
   - Go to GitHub Settings → Developer Settings → OAuth Apps → New OAuth App
   - Application Name: `CodeForge AI` (or your preferred name)
   - Homepage URL: `http://localhost:5173` (or your frontend URL)
   - Authorization callback URL: `http://localhost:5173/github/callback`

2. **Configure Backend**:
   - Copy the Client ID and Client Secret
   - Add to backend `application.properties`:
     ```properties
     github.client-id=your_client_id
     github.client-secret=your_client_secret
     github.redirect-uri=http://localhost:5173/github/callback
     ```

3. **Frontend Configuration**:
   - No additional frontend configuration needed
   - The OAuth flow is handled automatically via `authService.loginWithGithub()`

## Development Commands

```bash
# Install dependencies
npm install

# Start development server (with hot module replacement)
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run linter (oxlint)
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ai/             # AI-specific components (SemanticSearchPanel, etc.)
│   │   ├── common/         # Shared components (Spinner, ProgressBar, etc.)
│   │   ├── github/         # GitHub import components
│   │   ├── projects/       # Project management components
│   │   └── Navbar.tsx      # Main navigation bar
│   ├── context/            # React context providers
│   │   └── AuthContext.tsx # Authentication state and methods
│   ├── layouts/            # Layout components
│   │   └── MainLayout.tsx  # Main application layout with navbar
│   ├── pages/              # Page-level components (route targets)
│   │   ├── ai/             # AI chat and search pages
│   │   ├── auth/           # Login, register, OAuth callback
│   │   ├── candidate/      # Candidate-specific pages
│   │   ├── recruiter/      # Recruiter-specific pages
│   │   ├── admin/          # Admin dashboard and user management
│   │   └── github/         # GitHub repository import pages
│   ├── routes/             # Route protection and configuration
│   │   ├── ProtectedRoute.tsx  # Authentication-required routes
│   │   └── RoleRoute.tsx       # Role-based access control
│   ├── services/           # API communication layer
│   │   ├── api/            # Domain-specific API services
│   │   │   ├── aiService.ts        # AI chat and search endpoints
│   │   │   ├── githubService.ts    # GitHub OAuth and import
│   │   │   ├── projectService.ts   # Project CRUD operations
│   │   │   └── userService.ts      # User management (admin)
│   │   ├── apiClient.ts    # Axios instance with interceptors
│   │   └── authService.ts  # Authentication methods
│   ├── types/              # TypeScript type definitions
│   │   ├── auth.ts         # User, login, and auth types
│   │   ├── api.ts          # Common API response types
│   │   ├── github.ts       # GitHub repository types
│   │   └── project.ts      # Project and task types
│   ├── utils/              # Helper functions
│   │   ├── errorHandler.ts # Error parsing and formatting
│   │   └── toast.ts        # Toast notification helpers
│   ├── App.tsx             # Root component with routing
│   ├── App.css             # Global styles and CSS variables
│   └── main.tsx            # Application entry point
├── public/                 # Static assets
├── .env.example            # Environment variable template
├── .env.local              # Local environment config (gitignored)
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite build configuration
└── README.md               # This file
```

### Key Directories Explained

- **components/**: Organized by domain (ai, github, projects) and common reusable components
- **pages/**: Each page corresponds to a route and aggregates components
- **services/**: API layer with automatic JWT injection and snake_case ↔ camelCase conversion
- **types/**: TypeScript interfaces for all data models (matches backend DTOs)
- **routes/**: Route guards for authentication and role-based access control

## Styling

The application uses vanilla CSS with:

- **CSS Variables**: Defined in `App.css` for consistent theming
  ```css
  --color-primary: #0066cc
  --color-bg: #f5f5f5
  --color-muted: #999
  ```
- **Reusable Classes**: `.btn`, `.card`, `.alert`, etc. for common UI patterns
- **Component-Scoped CSS**: Each page/component has its own CSS file imported alongside

### Responsive Breakpoints
- **Mobile**: 480px and below
- **Tablet**: 768px and below
- **Desktop**: 1024px and above

## Backend Integration

### API Endpoints Summary

#### Authentication
- `POST /api/auth/login` - Email/password login
- `POST /api/auth/register` - Create new account
- `POST /api/auth/github` - GitHub OAuth login
- `POST /api/auth/logout` - Clear session

#### GitHub Integration
- `GET /api/github/authorize` - Start OAuth flow
- `POST /api/github/callback` - Handle OAuth callback
- `GET /api/github/user-repos` - List authenticated user's repositories
- `POST /api/github/import` - Clone and index repository

#### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

#### Code Search
- `POST /api/code/search` - Semantic code search with Qdrant

#### AI Chat
- `POST /api/v1/projects/{id}/ai/chat` - Send chat message
- `GET /api/v1/projects/{id}/ai/conversations` - List conversations
- `GET /api/v1/projects/{id}/ai/conversations/{convId}` - Get conversation details

#### Admin
- `GET /api/admin/users` - List all users
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user

### API Client Features

The `apiClient` in `src/services/apiClient.ts` provides:

- **JWT Token Injection**: Automatically adds `Authorization: Bearer <token>` header
- **Snake Case Conversion**: Converts camelCase request data to snake_case for backend
- **Camel Case Conversion**: Converts snake_case responses to camelCase for frontend
- **Error Handling**: Intercepts 401 responses and redirects to login
- **Base URL Configuration**: Uses `VITE_API_BASE_URL` from environment

### Authentication Flow

1. User logs in via email/password or GitHub OAuth
2. Backend returns JWT token
3. Token stored in `localStorage` as `token`
4. `apiClient` automatically injects token in all subsequent requests
5. `AuthContext` provides `user` object and `login`/`logout` methods
6. Protected routes redirect to `/login` if not authenticated
7. Role-based routes restrict access by user role (CANDIDATE, RECRUITER, ADMIN)

## Testing

Currently, the project uses manual browser testing:

1. Run `npm run dev` to start the development server
2. Test each feature in the browser
3. Use browser DevTools to test responsive breakpoints
4. Check console for errors and warnings
5. Verify API calls in Network tab

### Manual Test Checklist
- [ ] Login with email/password
- [ ] Login with GitHub OAuth
- [ ] Register new account
- [ ] Import GitHub repository (requires backend with GitHub OAuth configured)
- [ ] View import progress and completion
- [ ] Perform semantic code search
- [ ] Send AI chat message with code block in response
- [ ] Copy code from code block
- [ ] View message timestamps
- [ ] Navigate between chat conversations
- [ ] Test responsive layouts on mobile/tablet/desktop
- [ ] Admin user management (create, edit, delete users)

## Browser Requirements

- Modern browsers with ES2020+ support (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- HTTPS or localhost required for Clipboard API (copy-to-clipboard functionality)
- JavaScript enabled
- Cookies enabled (for authentication)

## Development Tips

### Adding New Pages
1. Create component in `src/pages/{domain}/{PageName}.tsx`
2. Create corresponding CSS file `{PageName}.css`
3. Add route in `src/App.tsx` with appropriate protection
4. Add navigation link in `Navbar.tsx` if needed

### Adding API Endpoints
1. Define types in `src/types/{domain}.ts`
2. Create service method in `src/services/api/{domain}Service.ts`
3. Use `apiClient.get/post/put/delete` for requests
4. Handle errors with `try/catch` and `extractErrorMessage` utility

### State Management Pattern
- Use `useState` for local component state
- Use `useEffect` for side effects and cleanup
- Use `AuthContext` for global auth state
- No Redux or other state management libraries

### Error Handling Pattern
```typescript
import { extractErrorMessage, showError } from '../../utils/errorHandler';

try {
  const result = await someApiCall();
  // Handle success
} catch (err) {
  const message = extractErrorMessage(err);
  showError(message);
}
```

## Troubleshooting

### Development Server Won't Start
- Check Node.js version (requires 18+)
- Delete `node_modules` and run `npm install` again
- Check for port conflicts (default 5173)

### API Calls Fail with 404
- Verify backend is running at configured `VITE_API_BASE_URL`
- Check browser console for actual request URL
- Verify environment variable is properly loaded (restart dev server after `.env.local` changes)

### GitHub OAuth Not Working
- Verify GitHub OAuth app callback URL matches exactly: `http://localhost:5173/github/callback`
- Check backend has correct `github.client-id` and `github.client-secret`
- Ensure backend redirect URI matches frontend callback URL

### Code Blocks Not Rendering
- Verify backend AI service returns code in markdown format: ` ```language\ncode\n``` `
- Check browser console for JavaScript errors
- Test with a simple code block: ` ```js\nconsole.log('test');\n``` `

### Copy Button Not Working
- Requires HTTPS or localhost (Clipboard API restriction)
- Check browser console for permission errors
- Some browsers block clipboard access - test in Chrome/Edge first

## Contributing

When contributing to the frontend:

1. Match existing code patterns and conventions
2. Use TypeScript strict mode (all types must be defined)
3. Keep components focused and single-responsibility
4. Use `apiClient` for all HTTP requests
5. Follow CSS patterns from `App.css`
6. Test responsive layouts at all breakpoints
7. Handle errors gracefully with user-friendly messages
8. Use lucide-react icons for consistency

## License

[Your License Here]

## Support

For issues, questions, or contributions, please [open an issue](https://github.com/your-repo/issues) on GitHub.
