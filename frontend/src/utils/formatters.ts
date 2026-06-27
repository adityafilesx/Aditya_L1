export const formatScientific = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '---';
  return val.toExponential(2);
};

export const formatFlux = (val: number | null | undefined, digits: number = 1): string => {
  if (val === null || val === undefined || isNaN(val)) return '---';
  return val.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
};

export const formatTimestamp = (val: string | null | undefined): string => {
  if (!val) return '---';
  try {
    const date = new Date(val);
    if (isNaN(date.getTime())) return '---';
    return date.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
  } catch {
    return '---';
  }
};

export const formatPercent = (val: number | null | undefined, digits: number = 1): string => {
  if (val === null || val === undefined || isNaN(val)) return '---';
  return `${(val * 100).toFixed(digits)}%`;
};

export const formatLatency = (val: number | null | undefined): string => {
  if (val === null || val === undefined || isNaN(val)) return '---';
  return `${val.toFixed(0)}ms`;
};
