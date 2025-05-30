// For formatting dates

const months = {
    "01": "jan",
    "02": "feb",
    "03": "mar",
    "04": "apr",
    "05": "may",
    "06": "jun",
    "07": "jul",
    "08": "aug",
    "09": "sep",
    "10": "oct",
    "11": "nov",
    "12": "dec"
}

export const getDate = () => {
    // get today's date
    const today = new Date();

    // get today's year
    const year = today.getFullYear();

    // get today's month, where the month is 0-based (i.e. jan is 0, etc)
    // padStart adds 0 to the head of the string if the length is < 2
    const month = months[String(today.getMonth() + 1).padStart(2, '0')];

    // get today's day
    // logic similar to month, but day starts at 1
    const day = String(today.getDate()).padStart(2, '0');

    // return the date in format "ddmmmyyyy" where mmm is a 3-letter
    // abbrevation of the month
    return `${day}${month}${year}`;
};