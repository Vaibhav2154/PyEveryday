import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PyEveryday - Automate Your Daily Tasks with Python',
  description: 'A comprehensive collection of Python scripts designed to simplify your daily routine. From automation to productivity tools, streamline your workflow with PyEveryday.',
  keywords: ['Python', 'automation', 'scripts', 'productivity', 'tools', 'open source', 'utilities', 'web scraping', 'data processing'],
  authors: [{ name: 'Vaibhav2154' }],
  creator: 'Vaibhav2154',
  publisher: 'PyEveryday',
  openGraph: {
    title: 'PyEveryday - Automate Your Daily Tasks with Python',
    description: 'A comprehensive collection of Python scripts designed to simplify your daily routine. From automation to productivity tools, streamline your workflow with PyEveryday.',
    url: 'https://github.com/Vaibhav2154/PyEveryday',
    siteName: 'PyEveryday',
    images: [
      {
        url: '/og-image.png', // You'll need to add this image
        width: 1200,
        height: 630,
        alt: 'PyEveryday - Python Scripts for Daily Automation',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'PyEveryday - Automate Your Daily Tasks with Python',
    description: 'A comprehensive collection of Python scripts designed to simplify your daily routine. From automation to productivity tools, streamline your workflow with PyEveryday.',
    images: ['/og-image.png'], // You'll need to add this image
    creator: '@vaibhav2154', // Replace with actual Twitter handle if available
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    // Add verification codes if needed
    // google: 'your-google-verification-code',
    // yandex: 'your-yandex-verification-code',
    // yahoo: 'your-yahoo-verification-code',
  },
  category: 'technology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* Additional meta tags for better SEO and performance */}
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="theme-color" content="#3b82f6" />
        
        {/* Preconnect to external domains for better performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="preconnect" href="https://github.com" />
        
        {/* Google Fonts */}
        <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet" />
        
        {/* Favicon and app icons */}
        <link rel="icon" href="/icon.png" />
        <link rel="apple-touch-icon" sizes="180x180" href="/icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/icon.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/icon.png" />
        <link rel="manifest" href="/site.webmanifest" />
        
        {/* Structured data for better SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              "name": "PyEveryday",
              "description": "A comprehensive collection of Python scripts designed to simplify your daily routine. From automation to productivity tools, streamline your workflow with PyEveryday.",
              "url": "https://github.com/Vaibhav2154/PyEveryday",
              "author": {
                "@type": "Person",
                "name": "Vaibhav2154"
              },
              "programmingLanguage": "Python",
              "operatingSystem": "Cross-platform",
              "applicationCategory": "DeveloperApplication",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              }
            })
          }}
        />
      </head>
      <body className="font-inter antialiased">
        {/* Skip to main content for accessibility */}
        <a 
          href="#main-content" 
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded-lg z-50 transition-all duration-300"
        >
          Skip to main content
        </a>
        
        {/* Main content wrapper */}
        <main id="main-content" className="relative">
          {children}
        </main>
        
        {/* Analytics script placeholder - replace with your analytics code */}
        {process.env.NODE_ENV === 'production' && (
          <>
            {/* Google Analytics example - replace with your tracking ID */}
            {/* <script
              async
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
            />
            <script
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
                `,
              }}
            /> */}
          </>
        )}
        
        {/* Service Worker registration for PWA capabilities */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js')
                    .then(function(registration) {
                      console.log('ServiceWorker registration successful');
                    })
                    .catch(function(err) {
                      console.log('ServiceWorker registration failed');
                    });
                });
              }
            `,
          }}
        />
      </body>
    </html>
  )
}