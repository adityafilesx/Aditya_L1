import { Icon } from '@components/common/Icon';

export function ShellPage() {
  return (
    <div className="w-full h-full p-10 flex flex-col items-center justify-center text-center opacity-20">
      <Icon name="space_dashboard" size="xl" className="mb-4" />
      <h3 className="font-display-lg text-[24px]">Mission Workspace Ready</h3>
      <p className="font-body-lg">Select an operational module from the sidebar to begin analysis.</p>
    </div>
  );
}
