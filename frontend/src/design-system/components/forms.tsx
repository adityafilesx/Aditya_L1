import React from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface FormFieldProps {
  label?: string;
  error?: string | boolean;
  success?: string | boolean;
  disabled?: boolean;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

// 1. TextInput
export interface TextInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>, FormFieldProps {}

export const TextInput: React.FC<TextInputProps> = ({
  label,
  error,
  success,
  disabled,
  className,
  size = 'md',
  type = 'text',
  ...rest
}) => {
  return (
    <div className={cn('flex flex-col w-full', className)}>
      {label && <label className="block font-label-caps text-[11px] text-on-surface-variant mb-1.5">{label}</label>}
      <input
        type={type}
        disabled={disabled}
        className={cn(
          'w-full bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2 font-data-mono text-xs focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 outline-none transition-all text-on-surface',
          error && 'border-error focus:border-error focus:ring-error/10',
          disabled && 'opacity-50 cursor-not-allowed',
          size === 'sm' && 'py-1 px-3',
          size === 'lg' && 'py-3 px-6 text-sm'
        )}
        {...rest}
      />
      {error && typeof error === 'string' && <span className="text-[10px] text-error font-semibold mt-1">{error}</span>}
    </div>
  );
};

// 2. SearchInput
export const SearchInput: React.FC<TextInputProps> = ({ className, size, ...rest }) => {
  return (
    <div className={cn('relative w-full', className)}>
      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant/40 leading-none">
        <Icon name="search" className="text-[18px]" />
      </span>
      <input
        type="text"
        className="w-full pl-10 pr-4 py-2 bg-surface-container-low border border-outline-variant rounded-lg font-data-mono text-xs focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 outline-none transition-all text-on-surface"
        {...rest}
      />
    </div>
  );
};

// 3. Dropdown
export interface DropdownProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'>, FormFieldProps {
  options: { value: string; label: string }[];
}

export const Dropdown: React.FC<DropdownProps> = ({
  label,
  options,
  error,
  disabled,
  className,
  size,
  ...rest
}) => {
  return (
    <div className={cn('flex flex-col w-full', className)}>
      {label && <label className="block font-label-caps text-[11px] text-on-surface-variant mb-1.5">{label}</label>}
      <select
        disabled={disabled}
        className={cn(
          'w-full bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2 font-data-mono text-xs focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 outline-none transition-all text-on-surface cursor-pointer',
          error && 'border-error',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        {...rest}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};

// 4. MultiSelect
export const MultiSelect: React.FC<DropdownProps & { selectedValues: string[]; onSelectionChange: (val: string[]) => void }> = ({
  label,
  options,
  selectedValues,
  onSelectionChange,
  className,
}) => {
  const toggleOption = (val: string) => {
    const isSelected = selectedValues.includes(val);
    if (isSelected) {
      onSelectionChange(selectedValues.filter((v) => v !== val));
    } else {
      onSelectionChange([...selectedValues, val]);
    }
  };

  return (
    <div className={cn('flex flex-col w-full', className)}>
      {label && <label className="block font-label-caps text-[11px] text-on-surface-variant mb-1.5">{label}</label>}
      <div className="flex flex-wrap gap-1.5 p-2 bg-surface-container-low border border-outline-variant rounded-lg min-h-10">
        {options.map((opt) => {
          const isSelected = selectedValues.includes(opt.value);
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => toggleOption(opt.value)}
              className={cn(
                'px-2 py-0.5 rounded text-[10px] font-label-caps font-bold transition-all border',
                isSelected
                  ? 'bg-primary-container text-white border-primary-container'
                  : 'bg-white text-on-surface-variant border-outline-variant'
              )}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
    </div>
  );
};

// 5. DatePicker
export const DatePicker: React.FC<TextInputProps> = ({ size, ...props }) => (
  <TextInput type="date" size={size} {...props} />
);

// 6. TimeRange
export const TimeRange: React.FC<{
  label?: string;
  startTime: string;
  endTime: string;
  onStartChange: (val: string) => void;
  onEndChange: (val: string) => void;
  className?: string;
}> = ({ label, startTime, endTime, onStartChange, onEndChange, className }) => (
  <div className={cn('flex flex-col w-full', className)}>
    {label && <label className="block font-label-caps text-[11px] text-on-surface-variant mb-1.5">{label}</label>}
    <div className="flex gap-2">
      <input
        type="time"
        value={startTime}
        onChange={(e) => onStartChange(e.target.value)}
        className="flex-1 bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2 font-data-mono text-xs outline-none text-on-surface"
      />
      <input
        type="time"
        value={endTime}
        onChange={(e) => onEndChange(e.target.value)}
        className="flex-1 bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2 font-data-mono text-xs outline-none text-on-surface"
      />
    </div>
  </div>
);

// 7. Checkbox
export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label: string;
  className?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({ label, className, disabled, ...rest }) => (
  <label className={cn('flex items-center gap-2 cursor-pointer select-none text-body-sm text-on-surface', disabled && 'opacity-50 cursor-not-allowed', className)}>
    <input type="checkbox" disabled={disabled} className="accent-primary rounded" {...rest} />
    <span>{label}</span>
  </label>
);

// 8. Toggle (Switch)
export const Toggle: React.FC<CheckboxProps> = ({ label, className, disabled, ...rest }) => (
  <div className={cn('flex items-center gap-4 py-2', className)}>
    <label className={cn('relative inline-flex items-center cursor-pointer', disabled && 'opacity-50 cursor-not-allowed')}>
      <input type="checkbox" disabled={disabled} className="sr-only peer" {...rest} />
      <div className="w-11 h-6 bg-surface-container-highest peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-container"></div>
      <span className="ml-3 font-body-sm text-on-surface">{label}</span>
    </label>
  </div>
);

// 9. Slider
export interface SliderProps extends FormFieldProps {
  min: number;
  max: number;
  step?: number;
  value: number;
  onChange: (val: number) => void;
}

export const Slider: React.FC<SliderProps> = ({ label, min, max, step = 1, value, onChange, className }) => (
  <div className={cn('flex flex-col w-full', className)}>
    {label && (
      <div className="flex justify-between items-center mb-1.5">
        <label className="block font-label-caps text-[11px] text-on-surface-variant">{label}</label>
        <span className="font-data-mono text-[11px] text-primary">{value}</span>
      </div>
    )}
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      className="w-full accent-primary bg-surface-container-highest h-1 rounded-lg cursor-pointer"
    />
  </div>
);

// 10. NumberInput
export const NumberInput: React.FC<TextInputProps> = ({ size, ...props }) => (
  <TextInput type="number" size={size} {...props} />
);

// 11. TextArea
export interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement>, FormFieldProps {}

export const TextArea: React.FC<TextAreaProps> = ({ label, error, disabled, className, ...rest }) => (
  <div className={cn('flex flex-col w-full', className)}>
    {label && <label className="block font-label-caps text-[11px] text-on-surface-variant mb-1.5">{label}</label>}
    <textarea
      disabled={disabled}
      className={cn(
        'w-full bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2 font-data-mono text-xs focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 outline-none transition-all text-on-surface resize-y min-h-[80px]',
        error && 'border-error',
        disabled && 'opacity-50 cursor-not-allowed'
      )}
      {...rest}
    />
  </div>
);

// 12. CommandInput (Console line/Prompt line style input)
export const CommandInput: React.FC<TextInputProps> = ({ className, size, ...rest }) => (
  <div className={cn('flex items-center bg-terminal-bg rounded-lg border border-outline/30 px-3 py-2 font-data-mono text-xs text-white', className)}>
    <span className="text-success font-bold mr-2">&gt;</span>
    <input
      type="text"
      className="flex-1 bg-transparent border-none outline-none text-white font-data-mono"
      {...rest}
    />
  </div>
);

// 13. FilterGroup
export const FilterGroup: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={cn('flex flex-wrap gap-2 items-center', className)}>{children}</div>
);
