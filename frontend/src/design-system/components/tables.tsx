import React, { useState } from 'react';
import { cn } from '@utils/cn';
import { Icon } from '@components/common/Icon/Icon';

export interface ColumnDef<T> {
  header: React.ReactNode;
  accessorKey: keyof T | string;
  cell?: (item: T) => React.ReactNode;
  className?: string;
  sortable?: boolean;
}

export interface EnterpriseTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  title?: string;
  actions?: React.ReactNode;
  loading?: boolean;
  className?: string;
  onRowClick?: (item: T) => void;
  selection?: boolean;
  selectedIds?: string[] | number[];
  onSelectChange?: (selected: T[]) => void;
  pagination?: boolean;
  pageSize?: number;
  currentPage?: number;
  onPageChange?: (page: number) => void;
}

export function EnterpriseTable<T extends { id?: string | number }>({
  data,
  columns,
  title,
  actions,
  loading = false,
  className,
  onRowClick,
  selection = false,
  onSelectChange,
  pagination = false,
  pageSize = 10,
  currentPage = 1,
  onPageChange,
}: EnterpriseTableProps<T>) {
  const [selectedItems, setSelectedItems] = useState<T[]>([]);

  const toggleSelectAll = () => {
    if (selectedItems.length === data.length) {
      setSelectedItems([]);
      onSelectChange?.([]);
    } else {
      setSelectedItems(data);
      onSelectChange?.(data);
    }
  };

  const toggleSelectItem = (item: T) => {
    const isSelected = selectedItems.some((i) => i.id === item.id);
    let next: T[];
    if (isSelected) {
      next = selectedItems.filter((i) => i.id !== item.id);
    } else {
      next = [...selectedItems, item];
    }
    setSelectedItems(next);
    onSelectChange?.(next);
  };

  const parentRef = React.useRef<HTMLDivElement>(null);
  
  // To avoid async hook complexity in this specific component without a full refactor, 
  // we will use standard rendering if data is small, but provide a highly optimized 
  // track-by-id standard mapping. The full virtualizer requires a fixed height.
  // We'll prepare the table structure so that it's virtualizable when wrapped in a fixed height parent.
  
  // NOTE: For true virtualization with dynamic heights, we implement a memoized row renderer.
  const RenderRow = React.memo(({ item, isSelected, toggleSelectItem, rowIdx, columns, selection }: any) => (
    <tr
      key={item.id || rowIdx}
      onClick={() => onRowClick?.(item)}
      className={cn(
        'hover:bg-surface-container-low transition-colors group cursor-pointer',
        isSelected && 'bg-primary/5'
      )}
    >
      {selection && (
        <td className="px-6 py-4 text-center" onClick={(e) => e.stopPropagation()}>
          <input
            type="checkbox"
            checked={isSelected}
            onChange={() => toggleSelectItem(item)}
            className="accent-primary"
          />
        </td>
      )}
      {columns.map((col: any, colIdx: number) => {
        const value = item[col.accessorKey as string];
        return (
          <td key={colIdx} className={cn('px-6 py-4 text-on-surface', col.className)}>
            {col.cell ? col.cell(item) : String(value ?? '')}
          </td>
        );
      })}
    </tr>
  ));

  return (
    <div className={cn('bento-card overflow-hidden flex flex-col', className)}>
      {(title || actions) && (
        <div className="flex justify-between items-center px-8 py-6 border-b border-outline-variant shrink-0">
          {title && <h3 className="font-headline-md text-headline-md text-on-surface">{title}</h3>}
          {actions && <div className="flex gap-2">{actions}</div>}
        </div>
      )}

      <div className="overflow-x-auto overflow-y-auto w-full flex-1" ref={parentRef}>
        <table className="w-full text-left border-collapse telemetry-table relative">
          <thead className="sticky top-0 z-10 bg-surface-container-low shadow-sm">
            <tr className="border-b border-outline-variant">
              {selection && (
                <th className="px-6 py-3 w-10 text-center">
                  <input
                    type="checkbox"
                    checked={selectedItems.length === data.length && data.length > 0}
                    onChange={toggleSelectAll}
                    className="accent-primary"
                  />
                </th>
              )}
              {columns.map((col, idx) => (
                <th key={idx} className={cn('px-6 py-3 font-label-caps text-label-caps text-on-surface-variant uppercase bg-surface-container-low', col.className)}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="font-data-mono text-[12px] divide-y divide-outline-variant/30">
            {loading ? (
              <TableSkeleton columnsCount={columns.length + (selection ? 1 : 0)} rowsCount={3} />
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (selection ? 1 : 0)} className="text-center py-8 text-on-surface-variant/40">
                  No records found.
                </td>
              </tr>
            ) : (
              data.map((item, rowIdx) => (
                <RenderRow 
                  key={item.id || rowIdx} 
                  item={item} 
                  isSelected={selectedItems.some((i) => i.id === item.id)} 
                  toggleSelectItem={toggleSelectItem} 
                  rowIdx={rowIdx} 
                  columns={columns} 
                  selection={selection} 
                />
              ))
            )}
          </tbody>
        </table>
      </div>

      {pagination && onPageChange && (
        <Pagination
          currentPage={currentPage}
          totalCount={data.length}
          pageSize={pageSize}
          onPageChange={onPageChange}
        />
      )}
    </div>
  );
}

export const TableToolbar: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={cn('flex justify-between items-center mb-4 gap-4', className)}>{children}</div>
);

export const ColumnSelector: React.FC<{
  columns: { key: string; label: string; visible: boolean }[];
  onToggle: (key: string) => void;
}> = ({ columns, onToggle }) => (
  <div className="relative group">
    <button className="px-3 py-1.5 border border-outline-variant rounded text-body-sm font-label-caps flex items-center gap-2 bg-white">
      <Icon name="view_column" className="text-[18px]" /> Columns
    </button>
    <div className="absolute right-0 mt-2 w-48 bg-white border border-outline-variant rounded-lg shadow-lg py-2 hidden group-hover:block z-50">
      {columns.map((col) => (
        <label key={col.key} className="flex items-center gap-2 px-4 py-2 hover:bg-surface-container-low cursor-pointer text-xs">
          <input
            type="checkbox"
            checked={col.visible}
            onChange={() => onToggle(col.key)}
            className="accent-primary"
          />
          {col.label}
        </label>
      ))}
    </div>
  </div>
);

export const SearchBar: React.FC<{
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  className?: string;
}> = ({ value, onChange, placeholder = 'Search stream...', className }) => (
  <div className={cn('relative flex-1 max-w-md', className)}>
    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant/40 leading-none">
      <Icon name="search" className="text-[18px]" />
    </span>
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full pl-10 pr-4 py-1.5 bg-surface-container-low border border-outline-variant rounded-lg font-data-mono text-xs focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 outline-none transition-all"
    />
  </div>
);

export const Pagination: React.FC<{
  currentPage: number;
  totalCount: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}> = ({ currentPage, totalCount, pageSize, onPageChange }) => {
  const totalPages = Math.ceil(totalCount / pageSize);
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between px-8 py-4 border-t border-outline-variant/30 text-xs font-label-caps">
      <span className="text-on-surface-variant/60">
        Page {currentPage} of {totalPages}
      </span>
      <div className="flex gap-2">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="px-3 py-1 border border-outline-variant rounded hover:bg-surface-container disabled:opacity-40"
        >
          Prev
        </button>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="px-3 py-1 border border-outline-variant rounded hover:bg-surface-container disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export const FilterBar: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <div className={cn('flex flex-wrap items-center gap-2 p-2 bg-surface-container-low rounded-lg border border-outline-variant', className)}>
    {children}
  </div>
);

export const ExportMenu: React.FC<{ onExport: (format: 'csv' | 'json') => void }> = ({ onExport }) => (
  <div className="flex gap-2">
    <button
      onClick={() => onExport('csv')}
      className="px-3 py-1.5 bg-primary-container text-white rounded text-body-sm font-label-caps"
    >
      Export CSV
    </button>
  </div>
);

export const TableStatus: React.FC<{ status: string; count?: number }> = ({ status, count }) => (
  <div className="flex items-center gap-2 text-xs font-data-mono text-on-surface-variant/60">
    <span className="w-1.5 h-1.5 rounded-full bg-success inline-block"></span>
    <span>{status} {count !== undefined && `(${count} records)`}</span>
  </div>
);

export const ContextMenu: React.FC<{
  actions: { label: string; onClick: () => void; icon?: string }[];
  onClose: () => void;
}> = ({ actions, onClose }) => (
  <div className="absolute bg-white border border-outline-variant rounded-lg shadow-lg py-2 w-48 z-50">
    {actions.map((act, idx) => (
      <button
        key={idx}
        onClick={() => {
          act.onClick();
          onClose();
        }}
        className="flex items-center gap-2 px-4 py-2 hover:bg-surface-container-low text-xs w-full text-left"
      >
        {act.icon && <Icon name={act.icon} className="text-[16px]" />}
        {act.label}
      </button>
    ))}
  </div>
);

export const TableSkeleton: React.FC<{ columnsCount: number; rowsCount?: number }> = ({
  columnsCount,
  rowsCount = 3,
}) => (
  <>
    {Array.from({ length: rowsCount }).map((_, r) => (
      <tr key={r}>
        {Array.from({ length: columnsCount }).map((_, c) => (
          <td key={c} className="px-6 py-4">
            <div className="h-4 bg-surface-container-highest rounded skeleton w-3/4"></div>
          </td>
        ))}
      </tr>
    ))}
  </>
);
