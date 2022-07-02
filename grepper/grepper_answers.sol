pragma solidity ^0.6.6;

//wrap code in
/*
    //grepper <search string>
    ...code...
    //end grepper
    */
// to automatically set the code as an answer to the search string
// the language will be deduced by the file extension

//grepper SafeERC20: low-level call failed
// if you are about to lend, swap, or deposit a token,
// check if you have approved the token contract with 
token = interface.IERC20(erc20_address)
tx = token.approve(approved_spender, amount, {"from": account})
// so that aprroved_spender can spend amount.
//
// if you have approved but still receiving an error,
// check if you have enought token amount to spend
// e.g. you approve to deposit 0.2 weth but you have only 0.1 weth in your balance
//end grepper
