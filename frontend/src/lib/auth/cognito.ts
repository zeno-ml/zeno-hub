import {
	zeno_user_pool_client_id,
	zeno_user_pool_id,
	zeno_user_pool_secret
} from '$env/static/private';
import {
	AuthenticationDetails,
	CognitoRefreshToken,
	CognitoUser,
	CognitoUserAttribute,
	CognitoUserPool,
	CognitoUserSession,
	type ISignUpResult
} from 'amazon-cognito-identity-js';
import { noop } from 'svelte/internal';

export type CognitoUserSessionType = CognitoUserSession;

const CONFIGS = {
	UserPoolId: zeno_user_pool_id,
	ClientId: zeno_user_pool_client_id,
	ClientSecret: zeno_user_pool_secret
};
const Pool = new CognitoUserPool(CONFIGS);

/**
 * Login to Cognito User Pool using the provided credentials.
 * This will return the session data at the time of login.
 *
 * @param Username - Email address of the user to login
 * @param Password - Password of the user to login
 * @returns - Promise with the result of the login
 */
export const getSession = (Username: string, Password: string): Promise<CognitoUserSession> => {
	return new Promise((resolve, reject) => {
		const user = new CognitoUser({ Username, Pool });
		user.authenticateUser(new AuthenticationDetails({ Username, Password }), {
			onSuccess: resolve,
			onFailure: reject
		});
	});
};

export function verify(Username: string, code: string) {
	const user = new CognitoUser({ Username, Pool });
	return new Promise((resolve, reject) => {
		user.confirmRegistration(code, false, function (err, result) {
			if (err) reject(err);
			else resolve(result);
		});
	});
}

export const resendCode = (Username: string) => {
	const user = new CognitoUser({ Username, Pool });
	user.resendConfirmationCode(noop);
};

/**
 * Refresh the access token of the provided user.
 *
 * @param sessionData - Session data of the user with the refresh token
 * @returns - Promise with the new user object with tokens and expiration date
 */
export const refreshAccessToken = async (sessionData: {
	refreshToken: string;
}): Promise<CognitoUserSession> => {
	const cognitoUser = Pool.getCurrentUser();
	// Check if the user is logged in
	if (!cognitoUser) {
		throw new Error('No user found');
	}
	// Refresh the session
	const RefreshToken = new CognitoRefreshToken({
		RefreshToken: sessionData.refreshToken
	});
	return new Promise<CognitoUserSession>((resolve) => {
		cognitoUser.refreshSession(RefreshToken, (_resp, session: CognitoUserSession) => {
			resolve(session);
		});
	});
};

export async function signUpUserWithEmail(
	username: string,
	email: string,
	password: string
): Promise<ISignUpResult | undefined> {
	return new Promise(function (resolve, reject) {
		const attributeList = [
			new CognitoUserAttribute({
				Name: 'email',
				Value: email
			})
		];

		Pool.signUp(username, password, attributeList, [], function (err, res) {
			if (err) {
				reject(err);
			} else {
				resolve(res);
			}
		});
	});
}
