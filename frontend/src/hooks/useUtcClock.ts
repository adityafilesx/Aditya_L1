import { useEffect, useState } from 'react';

export function useUtcClock(intervalMs = 100): string {
  const [time, setTime] = useState('00:00:00.000');

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setTime(now.toISOString().split('T')[1].replace('Z', ''));
    };

    update();
    const id = window.setInterval(update, intervalMs);
    return () => window.clearInterval(id);
  }, [intervalMs]);

  return time;
}

export function usePressScale<T extends HTMLElement>() {
  const onMouseDown = (event: React.MouseEvent<T>) => {
    event.currentTarget.style.transform = 'scale(0.98)';
  };

  const onMouseUp = (event: React.MouseEvent<T>) => {
    event.currentTarget.style.transform = 'scale(1)';
  };

  const onMouseLeave = (event: React.MouseEvent<T>) => {
    event.currentTarget.style.transform = 'scale(1)';
  };

  return { onMouseDown, onMouseUp, onMouseLeave };
}
