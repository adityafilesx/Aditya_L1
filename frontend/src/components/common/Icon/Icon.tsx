import { cn } from '@utils/cn';

type IconProps = {
  name: string;
  filled?: boolean;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
};

const sizeClasses = {
  sm: 'text-sm',
  md: 'text-xl',
  lg: 'text-[32px]',
  xl: 'text-[64px]',
};

export function Icon({ name, filled = false, className, size = 'md' }: IconProps) {
  return (
    <span
      className={cn(
        'material-symbols-outlined',
        filled && 'material-symbols-outlined--filled',
        sizeClasses[size],
        className,
      )}
      aria-hidden="true"
    >
      {name}
    </span>
  );
}
