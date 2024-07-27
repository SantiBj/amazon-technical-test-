interface Props {
    error: boolean;
    message: string | null;
  }
  
  export function AlertError({ error, message }: Props) {
    return (
      <>
        {error && (
          <div
            className="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50"
            role="alert"
          >
            <span className="font-medium w-[80%] mx-auto">{message}</span>
          </div>
        )}
      </>
    );
  }