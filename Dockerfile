# Dockerfile for project-8: AI-Powered Resume Builder
# This Dockerfile builds the Next.js application from the project-8 directory

# Use Node.js 18 LTS as base image
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app/project-8

# Copy project-8 package files
COPY project-8/package.json project-8/package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app/project-8
COPY --from=deps /app/project-8/node_modules ./node_modules
COPY project-8/ .

# Build the Next.js application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/project-8/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# Next.js standalone output is in .next/standalone
COPY --from=builder --chown=nextjs:nodejs /app/project-8/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/project-8/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Next.js standalone mode creates server.js in the standalone directory
CMD sh -c "node server.js"

