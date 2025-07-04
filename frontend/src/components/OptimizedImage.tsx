import React from 'react';
import Image from 'next/image';
import { useInView } from 'react-intersection-observer';
import { useImageOptimization } from '../hooks/useImageOptimization';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  quality?: number;
  priority?: boolean;
  className?: string;
}

const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width = 800,
  height = 600,
  quality = 85,
  priority = false,
  className = '',
}) => {
  const [ref, inView] = useInView({
    threshold: 0.1,
    triggerOnce: true,
  });

  const optimizedSrc = useImageOptimization(src, {
    width,
    height,
    quality,
  });

  return (
    <div
      ref={ref}
      className={`relative ${className}`}
      style={{
        width: width,
        height: height,
      }}
    >
      {inView && (
        <Image
          src={optimizedSrc}
          alt={alt}
          width={width}
          height={height}
          quality={quality}
          priority={priority}
          loading="lazy"
          placeholder="blur"
          blurDataURL={optimizedSrc}
        />
      )}
    </div>
  );
};

export default OptimizedImage;
