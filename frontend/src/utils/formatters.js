export function formatCurrency(value) {
    if (value == null) return "-";

    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 4,
    }).format(value);
}

export function formatDate(date) {
    if (!date) return "-";

    return new Date(date).toLocaleDateString();
}