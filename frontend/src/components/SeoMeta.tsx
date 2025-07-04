import React from 'react';
import { Helmet } from 'react-helmet-async';

interface SeoMetaProps {
  title: string;
  description: string;
  keywords?: string[];
  image?: string;
  url?: string;
  type?: 'website' | 'article' | 'product';
}

const SeoMeta: React.FC<SeoMetaProps> = ({
  title,
  description,
  keywords = [],
  image,
  url,
  type = 'website'
}) => {
  const baseUrl = process.env.REACT_APP_BASE_URL || window.location.origin;
  const fullUrl = url ? `${baseUrl}${url}` : window.location.href;
  const fullImage = image ? `${baseUrl}${image}` : null;

  const meta = {
    title: title,
    description: description,
    keywords: keywords.join(','),
    url: fullUrl,
    image: fullImage,
    type: type,
    site_name: 'ProThemesRU',
    author: 'ProThemesRU',
    publisher: 'ProThemesRU',
    twitter_creator: '@prothemesru',
    twitter_site: '@prothemesru'
  };

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{meta.title}</title>
      <meta name="description" content={meta.description} />
      <meta name="keywords" content={meta.keywords} />
      <meta name="author" content={meta.author} />
      <meta name="publisher" content={meta.publisher} />

      {/* Open Graph */}
      <meta property="og:title" content={meta.title} />
      <meta property="og:description" content={meta.description} />
      <meta property="og:type" content={meta.type} />
      <meta property="og:url" content={meta.url} />
      <meta property="og:site_name" content={meta.site_name} />
      {meta.image && <meta property="og:image" content={meta.image} />}

      {/* Twitter Cards */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:creator" content={meta.twitter_creator} />
      <meta name="twitter:site" content={meta.twitter_site} />
      <meta name="twitter:title" content={meta.title} />
      <meta name="twitter:description" content={meta.description} />
      {meta.image && <meta name="twitter:image" content={meta.image} />}

      {/* Canonical URL */}
      <link rel="canonical" href={meta.url} />

      {/* Schema.org */}
      <script type="application/ld+json">
        {JSON.stringify({
          '@context': 'https://schema.org',
          '@type': meta.type === 'article' ? 'Article' : 'WebSite',
          name: meta.title,
          description: meta.description,
          url: meta.url,
          image: meta.image,
          publisher: {
            '@type': 'Organization',
            name: meta.site_name,
            url: meta.url,
            logo: {
              '@type': 'ImageObject',
              url: `${baseUrl}/logo.png`,
              width: 1200,
              height: 630
            }
          }
        })}
      </script>
    </Helmet>
  );
};

export default SeoMeta;
