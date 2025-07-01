import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png"
import email_icon from "../assets/email.png"
import password_icon from "../assets/password.png"
import close_icon from "../assets/close.png"

const Register = () => {

  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setlastName] = useState("");


  const gohome = ()=> {
    window.location.href = window.location.origin;
  }

  const register = async (e) => {
    e.preventDefault();

    let register_url = window.location.origin+"/djangoapp/register";
    
    const res = await fetch(register_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "userName": userName,
            "password": password,
            "firstName":firstName,
            "lastName":lastName,
            "email":email
        }),
    });

    const json = await res.json();
    if (json.status) {
        sessionStorage.setItem('username', json.userName);
        window.location.href = window.location.origin;
    }
    else if (json.error === "Already Registered") {
      alert("The user with same username is already registered");
      window.location.href = window.location.origin;
    }
};

  return(
    <div className="register_container" style={{width: "50%"}}>
      <div className="header" style={{display: "flex",flexDirection: "row", justifyContent: "space-between"}}>
          <span className="text" style={{flexGrow:"1"}}>SignUp</span> 
          <div style={{display: "flex",flexDirection: "row", justifySelf: "end", alignSelf: "start" }}>
          <a href="/" onClick={()=>{gohome()}} style={{justifyContent: "space-between", alignItems:"flex-end"}}>
            <img style={{width:"1cm"}} src={close_icon} alt="X"/>
          </a>
          </div>
          <hr/>
        </div>

        <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} className="img_icon" alt='Username'/>
            <input type="text"  name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)}/>
          </div>
          <div>
            <img src={user_icon} className="img_icon" alt='First Name'/>
            <input type="text"  name="first_name" placeholder="First Name" className="input_field" onChange={(e) => setFirstName(e.target.value)}/>
          </div>

          <div>
            <img src={user_icon} className="img_icon" alt='Last Name'/>
            <input type="text"  name="last_name" placeholder="Last Name" className="input_field" onChange={(e) => setlastName(e.target.value)}/>
          </div>

          <div>
            <img src={email_icon} className="img_icon" alt='Email'/>
            <input type="email"  name="email" placeholder="email" className="input_field" onChange={(e) => setEmail(e.target.value)}/>
          </div>

          <div className="input">
            <img src={password_icon} className="img_icon" alt='password'/>
            <input name="psw" type="password"  placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)}/>
          </div>

        </div>
        <div className="submit_panel">
          <input className="submit" type="submit" value="Register"/>
        </div>
      </form>
      </div>
  )
}

export default Register;




// // Form.js
// import React, { useState } from 'react';
// import './Form.css';

// function Form() {
//     const [formData, setFormData] = useState({
//         username: '',
//         email: '',
//         password: '',
//         confirmPassword: '',
//     });

//     const [errors, setErrors] = useState({});

//     const handleChange = (e) => {
//         const { name, value } = e.target;
//         setFormData({
//             ...formData,
//             [name]: value,
//         });
//     };

//     const handleSubmit = (e) => {
//         e.preventDefault();
//         const newErrors = validateForm(formData);
//         setErrors(newErrors);

//         if (Object.keys(newErrors).length === 0) {
//             // Form submission logic here
//             console.log('Form submitted successfully!');
//         } else {
//             console.log('Form submission failed due to validation errors.');
//         }
//     };

//     const validateForm = (data) => {
//         const errors = {};

//         if (!data.username.trim()) {
//             errors.username = 'Username is required';
//         } else if (data.username.length < 4) {
//             errors.username = 'Username must be at least 4 characters long';
//         }

//         if (!data.email.trim()) {
//             errors.email = 'Email is required';
//         } else if (!/\S+@\S+\.\S+/.test(data.email)) {
//             errors.email = 'Email is invalid';
//         }

//         if (!data.password) {
//             errors.password = 'Password is required';
//         } else if (data.password.length < 8) {
//             errors.password = 'Password must be at least 8 characters long';
//         }

//         if (data.confirmPassword !== data.password) {
//             errors.confirmPassword = 'Passwords do not match';
//         }

//         return errors;
//     };

//     return (
//         <div className="form-container">
//             <h2 className="form-title">Form Validation</h2>
//             <form onSubmit={handleSubmit}>
//                 <div>
//                     <label className="form-label">
//                         Username:
//                     </label>
//                     <input
//                         className="form-input"
//                         type="text"
//                         name="username"
//                         value={formData.username}
//                         onChange={handleChange}
//                     />
//                     {errors.username && (
//                         <span className="error-message">
//                             {errors.username}
//                         </span>
//                     )}
//                 </div>
//                 <div>
//                     <label className="form-label">
//                         Email:
//                     </label>
//                     <input
//                         className="form-input"
//                         type="email"
//                         name="email"
//                         value={formData.email}
//                         onChange={handleChange}
//                     />
//                     {errors.email && (
//                         <span className="error-message">
//                             {errors.email}
//                         </span>
//                     )}
//                 </div>
//                 <div>
//                     <label className="form-label">
//                         Password:
//                     </label>
//                     <input
//                         className="form-input"
//                         type="password"
//                         name="password"
//                         value={formData.password}
//                         onChange={handleChange}
//                     />
//                     {errors.password && (
//                         <span className="error-message">
//                             {errors.password}
//                         </span>
//                     )}
//                 </div>
//                 <div>
//                     <label className="form-label">
//                         Confirm Password:
//                     </label>
//                     <input
//                         className="form-input"
//                         type="password"
//                         name="confirmPassword"
//                         value={formData.confirmPassword}
//                         onChange={handleChange}
//                     />
//                     {errors.confirmPassword && (
//                         <span className="error-message">
//                             {errors.confirmPassword}
//                         </span>
//                     )}
//                 </div>
//                 <button className="submit-button" type="submit">Submit</button>
//             </form>
//         </div>
//     );
// }

// export default Form;
