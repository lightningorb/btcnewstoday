
export function getUTCDateString() {
  const date = new Date();
  const year = date.getUTCFullYear();
  const month = date.getUTCMonth() + 1;  // months are zero-indexed
  const day = date.getUTCDate();
  return `${year}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
}
