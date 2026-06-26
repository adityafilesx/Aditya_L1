import React, { useState } from 'react';
import { cn } from '@utils/cn';

export interface LazyImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  alt: string;
  width: number | string;
  height: number | string;
  wrapperClassName?: string;
}

export const LazyImage: React.FC<LazyImageProps> = ({
  src,
  alt,
  width,
  height,
  className,
  wrapperClassName,
  ...props
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);

  return (
    <div
      className={cn('relative overflow-hidden bg-surface-container-low', wrapperClassName)}
      style={{ width, height, aspectRatio: typeof width === 'number' && typeof height === 'number' ? `${width}/${height}` : undefined }}
    >
      {!isLoaded && !error && (
        <div className="absolute inset-0 animate-pulse bg-surface-container" />
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center text-error bg-error/5">
          <span className="font-label-caps text-[10px]">Failed</span>
        </div>
      )}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading="lazy"
        decoding="async"
        onLoad={() => setIsLoaded(true)}
        onError={() => setError(true)}
        className={cn(
          'absolute inset-0 w-full h-full object-cover transition-opacity duration-300',
          isLoaded ? 'opacity-100' : 'opacity-0',
          className
        )}
        {...props}
      />
    </div>
  );
};
