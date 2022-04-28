#!/usr/bin/python
import os
import time
import logging
import functools
from typing import List, Any, Optional, Union, Tuple, Dict, Iterable
from non_fungible_manager_positions_return import NonFungibleManagerPositionsReseponse

from web3 import Web3
from web3.eth import Contract
from web3.contract import ContractFunction
from web3.exceptions import BadFunctionCallOutput, ContractLogicError
from web3.types import (
    TxParams,
    Wei,
    Address,
    ChecksumAddress,
    Nonce,
    HexBytes,
)

from uni_types import AddressLike

from util import (
    _str_to_addr,
    _addr_to_str,
    _validate_address,
    _load_contract,
    _load_contract_erc20,
    parse_nft_response_into_object,
    is_same_address,
)

from constants import (
    _netid_to_name,
    ETH_ADDRESS,
)

from config import (
    WALLET_ADDRESS,
    WALLET_PRIVATE_KEY,
)

PROVIDER='https://mainnet.infura.io/v3/49d9273a4f5c446697ee32b9af8bc7cc'

logger = logging.getLogger(__name__)


class UniswapV3:
    """
    Wrapper around UniswapV3 contracts.
    """

    w3: Web3
    use_estimate_gas: bool

    def __init__(
        self,
        address: Union[AddressLike, str, None] = WALLET_ADDRESS,
        private_key: Optional[str] = WALLET_PRIVATE_KEY,
        provider: str = PROVIDER,
        use_estimate_gas: bool = True,
        network: str = 'ETHEREUM',
        web3: Web3 = None,
        non_fungible_manager_contract_addr: str = None
    ) -> None:
        """
        :param address: The public address of the ETH wallet to use.
        :param private_key: The private key of the ETH wallet to use.
        :param provider: Can be optionally set to a Web3 provider URI. If none set, will fall back to the PROVIDER environment variable, or web3 if set.
        :param web3: Can be optionally set to a custom Web3 instance.
        :param network: Can be optionally set to other chains.
        :param non_fungible_manager_contract_addr: Can be optionally set to override the address of the factory contract.
        """
        self.address = _str_to_addr(
            WALLET_ADDRESS or "0x0000000000000000000000000000000000000000"
        )
        self.private_key = (
            WALLET_PRIVATE_KEY
            or "0x0000000000000000000000000000000000000000000000000000000000000000"
        )
        self.use_estimate_gas = use_estimate_gas

        if web3:
            self.w3 = web3
        else:
            # Initialize web3. Extra provider for testing.
            if not provider:
                provider = os.environ["PROVIDER"]
            self.w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))

        # Cache netid to avoid extra RPC calls
        self.netid = int(self.w3.net.version)
        if self.netid in _netid_to_name:
            self.netname = _netid_to_name[self.netid]
        else:
            raise Exception(f"Unknown netid: {self.netid}")
        logger.info(f"Using {self.w3} ('{self.netname}', netid: {self.netid})")

        # https://github.com/Uniswap/uniswap-v3-periphery/blob/main/deploys.md
        factory_contract_address = _str_to_addr(
            "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        )
        self.factory_contract = _load_contract(
            self.w3, abi_name="uniswap-v3/factory", address=factory_contract_address
        )
        quoter_addr = _str_to_addr("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")
        self.router_address = _str_to_addr(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        )
        self.quoter = _load_contract(
            self.w3, abi_name="uniswap-v3/quoter", address=quoter_addr
        )
        self.router = _load_contract(
            self.w3, abi_name="uniswap-v3/router", address=self.router_address
        )
        non_fungible_manager_contract_addr = _str_to_addr(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        )
        self.non_fungible_manager = _load_contract(
            self.w3, abi_name="uniswap-v3/nonfungiblemanager", address=non_fungible_manager_contract_addr
        )

    # ------ NFT Manager --------------------------------------------------------------------

    def list_positions(self): 
        """
        Function to get all the NFTs in the wallet.
        """
        uniswap_nft_counts = self.non_fungible_manager.functions.balanceOf("0xE39fDB722dCabCea5b764b483F524dE866f82253").call()
        nft_ids = []
        for index in range(uniswap_nft_counts):
            nft_id = self.non_fungible_manager.functions.tokenOfOwnerByIndex("0xE39fDB722dCabCea5b764b483F524dE866f82253", index).call()
            nft_ids.append(nft_id)

        id_to_info = {}       

        for nft_id in nft_ids:
            info = self.non_fungible_manager.functions.positions(nft_id).call()
            nft_info = parse_nft_response_into_object(info)
            id_to_info[nft_id] = nft_info

        return id_to_info

    # ------ Market --------------------------------------------------------------------
    # https://github.com/Uniswap/v3-sdk/blob/main/src/nonfungiblePositionManager.ts
    
    def mint(
        self,
        token0: AddressLike,
        token1: AddressLike,
        tickLower: int,
        tickUpper: int, 
        amount0Desired,
        amount1Desired,
        amount0Min,
        amount1Min,
        recipient,
        fee: int = 3000,
    ):        
        if token0 == token1:
            raise ValueError
        func_params = [token0, token1, fee, tickLower, tickUpper, amount0Desired, amount1Desired, amount0Min, amount1Min, recipient, self._deadline()]
        function = self.non_fungible_manager.functions.mint(*func_params)
        return self._build_and_send_tx(function)

    def increase_liquidity(self, token_id, liquidity, amount0, amount1) -> HexBytes:
        # tx_params = self._get_tx_params(max_eth)
        # max_token = int(max_eth * self.get_exchange_rate(token)) + 10

        pass

    def decrease_liquidity(self, token_id, liquidity, amount0, amount1):
        pass

    def collect(
        self, 
        token_id, 
        recipient, 
        amount0Max, 
        amount1Max
    ):
        pass

    def _get_tx_params(self, value: Wei = Wei(0), gas: Wei = None) -> TxParams:
        """Get generic transaction parameters."""
        params: TxParams = {
            "from": _addr_to_str(self.address),
            "value": value,
            "nonce": max(
                self.last_nonce, self.w3.eth.get_transaction_count(self.address)
            ),
        }
        if gas:
            params["gas"] = gas
        return params

    # ------ Approval Utils ------------------------------------------------------------
    def approve(self, token: AddressLike, max_approval: Optional[int] = None) -> None:
        """Give an exchange/router max approval of a token."""
        max_approval = self.max_approval_int if not max_approval else max_approval
        contract_addr = (
            self._exchange_address_from_token(token)
            if self.version == 1
            else self.router_address
        )
        function = _load_contract_erc20(self.w3, token).functions.approve(
            contract_addr, max_approval
        )
        logger.warning(f"Approving {_addr_to_str(token)}...")
        tx = self._build_and_send_tx(function)
        self.w3.eth.wait_for_transaction_receipt(tx, timeout=6000)

        # Add extra sleep to let tx propogate correctly
        time.sleep(1)

    def _is_approved(self, token: AddressLike) -> bool:
        """Check to see if the exchange and token is approved."""
        _validate_address(token)
        if self.version == 1:
            contract_addr = self._exchange_address_from_token(token)
        elif self.version in [2, 3]:
            contract_addr = self.router_address
        amount = (
            _load_contract_erc20(self.w3, token)
            .functions.allowance(self.address, contract_addr)
            .call()
        )
        if amount >= self.max_approval_check_int:
            return True
        else:
            return False

    # ------ Tx Utils ------------------------------------------------------------------
    def _deadline(self) -> int:
        """Get a predefined deadline. 10min by default (same as the Uniswap SDK)."""
        return int(time.time()) + 10 * 60

    def _build_and_send_tx(
        self, function: ContractFunction, tx_params: Optional[TxParams] = None
    ) -> HexBytes:
        """Build and send a transaction."""
        if not tx_params:
            tx_params = self._get_tx_params()
        transaction = function.buildTransaction(tx_params)

        if "gas" not in tx_params:
            # `use_estimate_gas` needs to be True for networks like Arbitrum (can't assume 250000 gas),
            # but it breaks tests for unknown reasons because estimateGas takes forever on some tx's.
            # Maybe an issue with ganache? (got GC warnings once...)
            if self.use_estimate_gas:
                # The Uniswap V3 UI uses 20% margin for transactions
                transaction["gas"] = Wei(
                    int(self.w3.eth.estimate_gas(transaction) * 1.2)
                )
            else:
                transaction["gas"] = Wei(250000)

        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        # TODO: This needs to get more complicated if we want to support replacing a transaction
        # FIXME: This does not play nice if transactions are sent from other places using the same wallet.
        try:
            return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        finally:
            logger.debug(f"nonce: {tx_params['nonce']}")
            self.last_nonce = Nonce(tx_params["nonce"] + 1)
            
if __name__ == "__main__":

    # Testing portion remove later
    testUni = UniswapV3()
    print(testUni.list_positions())