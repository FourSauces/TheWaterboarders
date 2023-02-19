import { WalletSelector } from "@aptos-labs/wallet-adapter-ant-design";
import { Layout, Row, Col, Button } from "antd";  
import "@aptos-labs/wallet-adapter-ant-design/dist/index.css";
import { AptosClient } from "aptos";
import { useWallet } from "@aptos-labs/wallet-adapter-react";
import React, { useState, useEffect } from 'react';
import aquaShotImage from './Aqua Shot_centered.png'; // import the image

const NODE_URL = "https://fullnode.testnet.aptoslabs.com";
const client = new AptosClient(NODE_URL);



function App() {
  const { account, signAndSubmitTransaction } = useWallet();
  const [accountHasList, setAccountHasList] = useState<boolean>(false);

  const fetchList = async () => {
    if (!account){
      const alertZ = document.getElementById('message');
      if(alertZ != null){
        alertZ.textContent="Please connect your Petra wallet";
      }
      return [];
    } else{
      const alertZ = document.getElementById('message');
      if(alertZ != null){
        alertZ.textContent="Petra wallet connected!";
      }
      return [];
    }
    /*
    // change this to be your module account address
    const moduleAddress = "0xcbddf398841353776903dbab2fdaefc54f181d07e114ae818b1a67af28d1b018";
    try {
      const TodoListResource = await client.getAccountResource(
        account.address,
        `${moduleAddress}::todolist::TodoList`
      );
      setAccountHasList(true);
    } catch (e: any) {
      setAccountHasList(false);
    }
    */
  };


  const donateFund = async () => {
    if (!account) return [];
    // build a transaction payload to be submited
    const payload = {
      type: "entry_function_payload",
      function: `0x1::coin::transfer`,
      type_arguments: ["0x1::aptos_coin::AptosCoin"],
      arguments: ["0x122bb03ce2fbad828339215cb406eb21e3439e6651fcd4dc8b225da17fa4958d", 10000000],//charges .1 APT
    };
    try {
      // sign and submit transaction to chain
      const response = await signAndSubmitTransaction(payload);
      // wait for transaction
      await client.waitForTransaction(response.hash);
    } catch (error: any) {
    }
    const alertZ = document.getElementById('message');
      if(alertZ != null){
        alertZ.textContent="Shot Purchased! Keep an eye on your offers to claim the NFT.";
      }
      return [];
  };

  useEffect(() => {
    fetchList();
  }, [account?.address]);




  return (
    <>
      <Layout >
        <Row align="middle" style={{ backgroundColor: "#ffffff" }}>
          <Col span={10} offset={3}>
          <h1 style={{ fontFamily: "Arial, sans-serif", fontSize: "60px", fontWeight: "bold", color: "#38A6DB" }}>Aqua Shot</h1>
          </Col>
          <Col span={20} style={{ textAlign: "right", backgroundColor: "#ffffff" }}>
            <WalletSelector />
          </Col>
        </Row>
        <Row align="middle" style={{ backgroundColor: "#38A6DB" }}>
        <Button onClick={donateFund} block type="primary" style={{ height: "80px", backgroundColor: "#38A6DB", color: "#ffffff", fontSize: "50px" } }>
          Click here to purchase a shot
        </Button>
        </Row>
        <Row align="middle" style={{ backgroundColor: "#ffffff" }}>
          <h1 id="message">
            Connect your wallet please
          </h1>
        </Row>
        <Row align="middle">
          
        </Row>
        

      </Layout>
    </>
  );
}

export default App;