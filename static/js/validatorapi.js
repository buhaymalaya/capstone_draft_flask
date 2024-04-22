// Phone and email validator - With our Phone and Email Validator, you verify and validate the 
// existence of any phone and email address online for free. Without sending any email or making a call… 
// Share this tool with your colleague, if you feel this can be productive for personal and professional use
// Now you can also Validate IP address and Also Validate Postal Code of ZipCode for USA from this API
// Will only validate emails for code below

document.getElementById('validate-btn').addEventListener('click', async () => {
    const email = document.getElementById('email-input').value.trim();
    if (!email) {
        console.error('Please enter an email address.');
        return;
    }

    const url = `https://phone-and-email-validator.p.rapidapi.com/?email=${encodeURIComponent(email)}`;
    const options = {
        method: 'GET',
        headers: {
            'X-RapidAPI-Key': '11b375a328mshb8b10913a45e28dp142ff2jsn273ededd9cee',
            'X-RapidAPI-Host': 'phone-and-email-validator.p.rapidapi.com'
        }
    };

    try {
        const response = await fetch(url, options);
        const result = await response.text();
        console.log(result);
    } catch (error) {
        console.error(error);
    }
});
