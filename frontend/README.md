# Frontend Setup

## Prerequisites

- Node.js 18+
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install
```

2. Set environment variables:
```bash
export NEXT_PUBLIC_BACKEND_ENDPOINT=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Build for Production

```bash
npm run build
npm start
```

## Customization

The frontend uses Tailwind CSS for styling. You can customize:
- Colors and themes in `tailwind.config.js`
- Global styles in `styles/globals.css`
- Component-specific styles in individual component files
