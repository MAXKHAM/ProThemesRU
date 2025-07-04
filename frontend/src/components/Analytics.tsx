import React from 'react';

const Analytics: React.FC = () => {
  React.useEffect(() => {
    // Google Analytics
    const gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${process.env.REACT_APP_GOOGLE_ANALYTICS_ID}`;
    document.head.appendChild(gaScript);

    const gaInit = document.createElement('script');
    gaInit.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${process.env.REACT_APP_GOOGLE_ANALYTICS_ID}');
    `;
    document.head.appendChild(gaInit);

    // Яндекс Метрика
    const yaScript = document.createElement('script');
    yaScript.type = 'text/javascript';
    yaScript.async = true;
    yaScript.src = `https://mc.yandex.ru/metrika/tag.js`;
    document.head.appendChild(yaScript);

    const yaInit = document.createElement('script');
    yaInit.innerHTML = `
      var yaCounter = new Ya.Metrika({
        id: ${process.env.REACT_APP_YANDEX_METRIKA_ID},
        clickmap: true,
        trackLinks: true,
        accurateTrackBounce: true,
        webvisor: true
      });
    `;
    document.head.appendChild(yaInit);

    return () => {
      document.head.removeChild(gaScript);
      document.head.removeChild(gaInit);
      document.head.removeChild(yaScript);
      document.head.removeChild(yaInit);
    };
  }, []);

  return null;
};

export default Analytics;
