export const SERVER_BASE_URL =
  process.env.NODE_ENV === 'development'
    ? process.env.NEXT_PUBLIC_SERVER_URL
    : process.env.NEXT_PUBLIC_SERVER_URL || '';