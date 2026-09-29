export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return <div className="page-loading">{label}</div>;
}
