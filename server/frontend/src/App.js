
// // added from cpt:
// import React from "react";
// import LoginPanel from "./components/Login/Login"
// import { Routes, Route } from "react-router-dom";
// import Register from "./components/Register/Register";
// // import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; // added by chatgpt
// import Dealers from './components/Dealers/Dealers';
// import Dealer from "./components/Dealers/Dealer"

// function App() {
//   return (
//     <Routes>
//       <Route path="/login" element={<LoginPanel />} />
//       <Route path="/register" element={<Register />} /> 
//       {/* blew added by chatgpt */}
//       <Route path="/" element={<h1>Welcome to My-Dealership!</h1>} /> 
//       <Route path="/dealers" element={<Dealers/>}   /> 
//       <Route path="/dealer/:id" element={<Dealer/>} />
//     </Routes>
//   );
// }
// export default App;
// // app.use('/api/reviews', require('./routes/reviews'));
//++++++++++  gemini
// import React from "react";
// import LoginPanel from "./components/Login/Login"
// import { Routes, Route } from "react-router-dom";
// import Register from "./components/Register/Register";
// import Dealers from './components/Dealers/Dealers';
// import Dealer from "./components/Dealers/Dealer"

// function App() {
//   console.log("App component rendered"); // ADD THIS LINE

//   return (
//     <Routes>
//       <Route path="/login" element={<LoginPanel />} />
//       <Route path="/register" element={<Register />} />
//       <Route path="/" element={<h1>Welcome to My-Dealership!</h1>} />
//       <Route path="/dealers" element={() => { // MODIFY THIS LINE
//         console.log("Dealers component will render"); // ADD THIS LINE
//         return <Dealers />;
//       }}   />
//       <Route path="/dealer/:id" element={<Dealer/>} />
//     </Routes>
//   );
// }
// export default App;
import React from "react";
import LoginPanel from "./components/Login/Login";
import { Routes, Route } from "react-router-dom";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview"


function App() {
  console.log("App component rendered");

  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<h1>Welcome to My-Dealership!</h1>} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview/>} />
    </Routes>
  );
}

export default App;
