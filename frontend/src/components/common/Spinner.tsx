import { Loader } from "lucide-react";

interface SpinnerProps {
  size?: number;
}

export function Spinner({ size = 24 }: SpinnerProps) {
  return (
    <Loader
      size={size}
      style={{
        animation: "spin 1s linear infinite",
      }}
    />
  );
}
