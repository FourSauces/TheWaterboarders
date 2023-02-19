import { WalletSelector } from "@aptos-labs/wallet-adapter-ant-design";
import { Layout, Row, Col, Button } from "antd";  
import "@aptos-labs/wallet-adapter-ant-design/dist/index.css";
import { AptosClient } from "aptos";
import { useWallet } from "@aptos-labs/wallet-adapter-react";
import React, { useState, useEffect } from 'react';


const NODE_URL = "https://fullnode.testnet.aptoslabs.com";
const client = new AptosClient(NODE_URL);



function App() {
  const { account, signAndSubmitTransaction } = useWallet();
  const [accountHasList, setAccountHasList] = useState<boolean>(false);

  const fetchList = async () => {
    if (!account) return [];
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
  };

  useEffect(() => {
    fetchList();
  }, [account?.address]);
  return (
    <>
      <Layout>
        <Row align="middle">
          <Col span={10} offset={2}>
            <h1>Aqua Shot</h1>
          </Col>
          <Col span={12} style={{ textAlign: "right", paddingRight: "200px" }}>
            <Col span={12} style={{ textAlign: "right", paddingRight: "200px" }}>
            <WalletSelector />
          </Col>
          </Col>
        </Row>
        <Button onClick={donateFund} block type="primary" style={{ height: "40px", backgroundColor: "#3f67ff" }}>
          Purchase a shot
        </Button>
      </Layout>
    </>
  );
}

export default App;