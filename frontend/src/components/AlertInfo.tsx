export function AlertInfo({ text }: { text: string }) {
    return (
      <section className="p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50">
        {text}
      </section>
    );
  }
  